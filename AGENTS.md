# AGENTS.md — web del grup HuPBA (repositori públic)

Instruccions per a qualsevol agent o persona que treballi en aquest repositori. És la **font de veritat** de les normes de treball; `CLAUDE.md` només hi afegeix detalls específics de Claude Code, i `DESIGN.md` recull les decisions de disseny.

## Què és això
Web estàtica del grup de recerca HuPBA (Human Pose Recovery and Behavior Analysis, Universitat de Barcelona / Computer Vision Center), publicada amb GitHub Pages a https://hupba.github.io/. HTML + CSS pla, generat per scripts de Python sense dependències (`scripts/build_site.py`).

## Repositori **públic**: regles dures
- Res de dades privades: **cap correu, telèfon, adreça, credencial, token ni nota interna**. Només el que ja és públic i d'ús raonable.
- Cada afirmació sobre una persona (rol, pertinença, dates) ha de tenir una **font pública** (URL).
- No es publiquen fotos ni dades de persones que no siguin ja públiques; davant del dubte, no es publica i es pregunta.
- Idioma de la web: anglès. Idioma de treball (commits, issues, docs interns): català.

## Estructura
- `templates/page.html` + `content/*.html` + `data/people.json`: **fonts** de les pàgines. `index.html`, `people.html`, `research.html`, `projects.html`, `events.html` s'**generen** (no s'editen a mà).
- `assets/style.css`, `assets/img/`: estil i imatges.
- `data/people.json`: **font de veritat de les persones** (vegeu més avall). les pàgines (Home i People) es generen d'aquí.
- `scripts/`: validació i generació.
- `.claude/agents/`: agents especialitzats (disseny i accessibilitat; recerca d'informació).

## Persones: model de dades (`data/people.json`)
Cada persona: `id` (slug únic), `name`, `aliases`, `status` (`current`/`former`), `roles[]` (`role`, `from`, `to`, **`source`** obligatòria), `website`, `links` (scholar, dblp, orcid, github, linkedin…), `photo`, `affiliation`, `notes`, `verified` (data AAAA-MM-DD de l'última verificació, o `null`).
Rols vàlids: `director`, `senior-member`, `postdoc`, `phd-student`, `master-student`, `research-assistant`, `visiting`, `collaborator`. El rol actual és l'**últim** de la llista; si `status` és `current`, no pot tenir `to`.

### Com es recull i es manté la informació
1. **Fonts, per ordre de preferència**: web personal de la persona → perfils acadèmics (ORCID, DBLP, Google Scholar, Semantic Scholar/OpenAlex) → web del director (sergioescalera.com/students/) → web de la UB/CVC → web antiga de HuPBA (Wayback).
2. L'agent d'investigació (`.claude/agents/investigador.md`) **proposa** canvis amb font i nivell de confiança; no els aplica sense revisió humana.
3. Un canvi només es considera verificat quan hi ha una font pública que el sosté: llavors s'actualitza `verified`.
4. **Contradiccions**: si dues fonts discrepen (rol, dates, pertinença), no es tria en silenci: s'anota a `notes` i s'escala a una persona.
5. **Duplicats**: es detecten per nom/àlies normalitzats (sense accents ni majúscules) i per web/enllaços compartits. Una persona = una fitxa; les variants del nom van a `aliases`.
6. **Actualització periòdica**: `python3 scripts/validate_people.py --online` (avisa de verificacions antigues >365 dies i webs inaccessibles).

### Ordres
```bash
python3 scripts/validate_people.py            # esquema, duplicats, contradiccions, fonts, privacitat
python3 scripts/validate_people.py --online   # a més, comprova que les webs responen
python3 scripts/build_site.py                 # regenera les pàgines HTML
python3 scripts/build_site.py --check         # falla si alguna pàgina no està al dia
```
Abans de cada commit: validar i regenerar. El CI (`.github/workflows/validate.yml`) ho comprova.

## Flux de treball
- Canvis petits i revisables; un commit per tema. No pujar res que no hagi passat la validació.
- Disseny i accessibilitat: seguir `DESIGN.md`; en canvis visuals, revisar amb l'agent de disseny i accessibilitat.
- Decisions noves (disseny, estructura, dades) → es registren al fitxer corresponent (`DESIGN.md` o aquest) en el mateix commit.
