#!/usr/bin/env python3
"""Valida data/people.json: esquema, duplicats, contradiccions, fonts, privacitat.
Ús:  python3 scripts/validate_people.py [--online] [--stale-days 365]
Surt amb codi 1 si hi ha errors (els avisos no fallen)."""
import sys, re, datetime, urllib.request
from collections import defaultdict
from people_lib import *

errors, warns = [], []
E = lambda m: errors.append(m); W = lambda m: warns.append(m)
online = "--online" in sys.argv
stale = int(sys.argv[sys.argv.index("--stale-days")+1]) if "--stale-days" in sys.argv else 365
today = datetime.date.today()
EMAIL = re.compile(r"[\w.+-]+(@| ?\(at\) ?| \[at\] )[\w-]+(\.| ?\(dot\) ?)[\w.-]+", re.I)
URL = re.compile(r"^https?://\S+$")

def date_ok(v):
    if v is None: return True
    return isinstance(v, str) and re.fullmatch(r"\d{4}(-\d{2}(-\d{2})?)?", v) is not None

people = load()
ids, names, sites = {}, defaultdict(list), defaultdict(list)
for p in people:
    i = p.get("id", "?")
    for k in ("id", "name", "status", "roles"):
        if k not in p: E(f"{i}: falta el camp '{k}'")
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", i): E(f"{i}: id no vàlid (slug en minúscules)")
    if i in ids: E(f"{i}: id duplicat")
    ids[i] = p
    if p.get("status") not in STATUS: E(f"{i}: status ha de ser {STATUS}")
    # noms i àlies -> detecció de duplicats
    for n in [p.get("name", "")] + p.get("aliases", []):
        names[fold(n)].append(i)
    # web
    w = p.get("website")
    if w:
        if not URL.match(w): E(f"{i}: website no és una URL http(s)")
        sites[norm_url(w)].append(i)
    for k, v in p.get("links", {}).items():
        if k not in LINK_KEYS: W(f"{i}: clau d'enllaç desconeguda '{k}'")
        if not URL.match(v): E(f"{i}: enllaç '{k}' no és una URL")
        else: sites[norm_url(v)].append(i)
    # rols
    roles = p.get("roles", [])
    if not roles: E(f"{i}: cal almenys un rol")
    for r in roles:
        if r.get("role") not in ROLES: E(f"{i}: rol desconegut '{r.get('role')}' (vàlids: {ROLES})")
        for d in ("from", "to"):
            if not date_ok(r.get(d)): E(f"{i}: data '{d}' ha de ser AAAA[-MM[-DD]] o null")
        if r.get("from") and r.get("to") and r["from"] > r["to"]: E(f"{i}: rol amb from > to")
        if not r.get("source") or not URL.match(r["source"]): E(f"{i}: cada rol necessita una font (URL)")
    # coherència estat <-> rols
    if roles:
        last = roles[-1]
        if p.get("status") == "current" and last.get("to"): E(f"{i}: actual però l'últim rol té data de fi")
        if p.get("status") == "former" and not last.get("to"): W(f"{i}: antic sense data de fi (desconeguda?)")
    if sum(1 for r in roles if r.get("role") == "director") and p.get("status") == "current":
        pass
    # foto
    ph = p.get("photo")
    if ph and not (ROOT / "assets" / "img" / "members" / ph).exists(): E(f"{i}: la foto '{ph}' no existeix")
    # verificació
    v = p.get("verified")
    if v is None: W(f"{i}: sense verificar")
    elif not date_ok(v): E(f"{i}: 'verified' no és una data")
    else:
        try:
            age = (today - datetime.date.fromisoformat(v if len(v) == 10 else v + "-01")).days
            if age > stale: W(f"{i}: verificació antiga ({age} dies)")
        except ValueError: E(f"{i}: 'verified' no és una data vàlida")
    # privacitat: cap correu a les dades públiques
    if EMAIL.search(str(p)): E(f"{i}: sembla contenir un correu electrònic (no es publiquen)")

for n, l in names.items():
    if len(set(l)) > 1: E(f"possible duplicat per nom/àlies '{n}': {sorted(set(l))}")
    elif len(l) > 1 and len(set(l)) == 1: W(f"{l[0]}: nom/àlies repetit dins la mateixa fitxa")
for s, l in sites.items():
    if len(set(l)) > 1: E(f"web/enllaç compartit per diverses persones '{s}': {sorted(set(l))}")
ndir = [p["id"] for p in people if p.get("status") == "current" and any(r.get("role") == "director" for r in p.get("roles", [])[-1:])]
if len(ndir) != 1: E(f"ha d'haver-hi exactament un director actual (ara: {ndir})")

if online:
    for p in people:
        w = p.get("website")
        if not w: continue
        try:
            req = urllib.request.Request(w, headers={"User-Agent": "Mozilla/5.0 (HuPBA link check)"})
            code = urllib.request.urlopen(req, timeout=15).status
            if code >= 400: W(f"{p['id']}: {w} -> HTTP {code}")
        except Exception as e:
            W(f"{p['id']}: {w} no accessible ({type(e).__name__})")

for m in errors: print("ERROR", m)
for m in warns: print("AVÍS ", m)
print(f"{len(people)} persones · {len(errors)} errors · {len(warns)} avisos")
sys.exit(1 if errors else 0)
