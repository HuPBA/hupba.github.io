#!/usr/bin/env python3
"""Genera el contingut de people.html a partir de data/people.json.
Ús:  python3 scripts/build_people.py [--check]   (--check falla si people.html no està al dia)"""
import re, sys, html
from people_lib import *
GROUP = lambda p: ("Former members" if p["status"] == "former" else
    {"director": "Head of the group", "senior-member": "Senior members", "postdoc": "Senior members",
     "phd-student": "PhD students"}.get(p["roles"][-1]["role"], "Other members"))
ORDER = ["Head of the group", "Senior members", "PhD students", "Other members", "Former members"]
groups = {g: [] for g in ORDER}
for p in load(): groups[GROUP(p)].append(p)
out = ["    <h1>People</h1>"]
for g in ORDER:
    if not groups[g]: continue
    out.append(f"    <h3>{g}</h3>\n    <ul class=\"people\">")
    for p in groups[g]:
        n = html.escape(p["name"])
        pic = (f'<img src="assets/img/members/{p["photo"]}" alt="" width="48" height="48" loading="lazy">' if p.get("photo")
               else f'<span class="ph" aria-hidden="true">{"".join(w[0] for w in p["name"].split()[:2])}</span>')
        inner = f"{pic}<span>{n}</span>"
        w = p.get("website")
        out.append("      <li>" + (f'<a href="{html.escape(w)}" rel="noopener">{inner}</a>' if w else f'<div class="np">{inner}</div>') + "</li>")
    out.append("    </ul>")
new = "\n".join(out)
f = ROOT / "people.html"; s = f.read_text(encoding="utf-8")
res = re.sub(r"(<main>\n).*?(\n  </main>)", lambda m: m.group(1) + new + m.group(2), s, flags=re.S)
if "--check" in sys.argv:
    if res != s: print("people.html no està al dia: executa scripts/build_people.py"); sys.exit(1)
    print("people.html al dia")
else:
    f.write_text(res, encoding="utf-8"); print("people.html regenerat")
