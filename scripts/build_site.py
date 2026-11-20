#!/usr/bin/env python3
"""Genera les pàgines HTML a partir de templates/page.html, content/*.html i data/people.json.
Ús:  python3 scripts/build_site.py [--check]   (--check falla si alguna pàgina no està al dia)"""
import sys, html
from people_lib import *

PAGES = [("index.html", "Home", None), ("people.html", "People", "People"), ("research.html", "Research", "Research"),
         ("projects.html", "Projects", "Projects"), ("events.html", "Events", "Events")]
tpl = (ROOT / "templates" / "page.html").read_text(encoding="utf-8")

def pic(p, size):
    if p.get("photo"):
        return f'<img src="assets/img/members/{p["photo"]}" alt="" width="{size}" height="{size}" loading="lazy">'
    return f'<span class="ph" aria-hidden="true">{"".join(w[0] for w in p["name"].split()[:2])}</span>'

def role_group(p):
    if p["status"] == "former": return "Former members"
    return {"director": "Head of the group", "senior-member": "Senior members", "postdoc": "Senior members",
            "phd-student": "PhD students"}.get(p["roles"][-1]["role"], "Other members")

def people_main(people):
    order = ["Head of the group", "Senior members", "PhD students", "Other members", "Former members"]
    g = {k: [] for k in order}
    for p in people: g[role_group(p)].append(p)
    out = []
    for k in order:
        if not g[k]: continue
        out.append(f'<h2>{k}</h2>\n<ul class="people">')
        for p in g[k]:
            inner = f'{pic(p, 56)}<span>{html.escape(p["name"])}</span>'
            w = p.get("website")
            out.append("  <li>" + (f'<a href="{html.escape(w)}" rel="noopener">{inner}</a>' if w else f'<div class="np">{inner}</div>') + "</li>")
        out.append("</ul>")
    return "\n".join(out)

def faces(people):
    cur = [p for p in people if p["status"] == "current" and p.get("photo")]
    items = "".join(f'<li><img src="assets/img/members/{p["photo"]}" alt="{html.escape(p["name"])}" title="{html.escape(p["name"])}" width="56" height="56" loading="lazy"></li>' for p in cur)
    return f'<ul class="faces">{items}</ul>'

HOME_HERO = '''<section class="hero">
  <div class="wrap">
    <div class="hero-text">
      <h1>HuPBA</h1>
      <p class="expand">Human Pose Recovery and Behavior Analysis</p>
      <p>A multidisciplinary research group in deep learning and computer vision, led by <a href="https://sergioescalera.com" rel="noopener">Sergio Escalera</a>, at the <a href="https://mat.ub.edu/en" rel="noopener">Universitat de Barcelona</a> and the <a href="https://cvc.uab.es" rel="noopener">Computer Vision Center</a>.</p>
    </div>
    <img class="motif" src="assets/img/motif.svg" alt="" width="220" height="250">
  </div>
</section>'''
def band(h1): return f'<section class="band"><div class="wrap"><h1>{h1}</h1></div></section>'

def render():
    people = load(); out = {}
    for f, name, h1 in PAGES:
        nav = "\n".join(f'      <a href="{pf}"{" aria-current=\"page\"" if pf == f else ""}>{pn}</a>' for pf, pn, _ in PAGES[1:])
        if f == "index.html": main = (ROOT/"content/home.html").read_text(encoding="utf-8").replace("{{faces}}", faces(people)); hero = HOME_HERO
        elif f == "people.html": main = people_main(people); hero = band(h1)
        else: main = (ROOT/"content"/f).read_text(encoding="utf-8"); hero = band(h1)
        title = "HuPBA Research Group" if f == "index.html" else f"{name} · HuPBA Research Group"
        out[f] = tpl.replace("{{title}}", title).replace("{{nav}}", nav).replace("{{hero}}", hero).replace("{{main}}", main)
    return out

bad = False
for f, content in render().items():
    p = ROOT / f
    if "--check" in sys.argv:
        if not p.exists() or p.read_text(encoding="utf-8") != content: print(f"{f} no està al dia"); bad = True
    else: p.write_text(content, encoding="utf-8")
if "--check" in sys.argv: print("pàgines al dia" if not bad else "executa scripts/build_site.py"); sys.exit(1 if bad else 0)
print("pàgines generades")
