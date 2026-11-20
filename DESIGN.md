# DESIGN.md — decisions de disseny

Registre viu. Cada decisió: què, per què. Si canvia, s'edita aquí i s'indica la data.

## Principis
1. **Contingut primer, amb vida visual.** La web serveix per trobar gent, línies de recerca i projectes, però ha de semblar moderna i viva, no un full estàtic de continguts (*Xavier, 2026-11-20: la versió serif "clàssica" semblava antiquada i sense vida*).
2. **No és una landing page.** El **menú és sempre visible** (cap hamburguesa, també en mòbil) i la Home és una porta d'entrada a continguts reals, no una pàgina de màrqueting: sense crides a l'acció, sense hero a pantalla completa (*Stanford SVL se'n va descartar per això*).
3. **Sense text de farciment ni meta-navegació.** Prohibits "See the people, our research…", "Welcome to…", "coming soon", "will be announced here". Una secció sense contingut real **no existeix** (ni s'hi enllaça).
4. **Tot el que es mostra és verificable** (vegeu `AGENTS.md`, secció Persones).
5. **Lleuger i durable**: HTML i CSS pla, sense frameworks ni JavaScript; es genera amb scripts de Python sense dependències.
6. **La vida visual ve de contingut propi i d'efectes discrets**: degradats suaus, una il·lustració pròpia (esquelet de pose + malla topològica, `assets/img/motif.svg`), cares de les persones, línies d'accent. Quan hi hagi figures de recerca o fotos de grup reals, s'hi donarà protagonisme.

## Estat actual (2026-11-20)
Home: banda amb degradat blau→cian (el nom HuPBA, l'expansió, una frase, il·lustració) + Research (2 línies), Projects (3) i People (cares). Resta de pàgines: banda amb títol i contingut en una columna de 62rem. Tipografia sans de sistema; mode fosc automàtic; pastilla de degradat a la pàgina activa. **Pendent**: figures de recerca / foto de grup, publicacions, i decidir si hi ha notícies.

## Implementació
Fitxers font: `templates/page.html` (estructura comuna), `content/*.html` (cos de cada pàgina), `data/people.json` (persones). **No s'editen els `*.html` de l'arrel**: es generen amb `python3 scripts/build_site.py`.

## Accessibilitat (requisits mínims, WCAG 2.2 AA)
- Contrast de text ≥ 4.5:1 (3:1 text gran) en mode clar i fosc.
- Navegació completa amb teclat; focus visible; enllaç "saltar al contingut" quan hi hagi més d'un bloc de navegació.
- Estructura semàntica: un sol `<h1>` per pàgina, jerarquia de títols sense salts, `<nav>`, `<main>`, `<footer>`.
- Imatges: `alt` descriptiu; les fotos de persones són decoratives si el nom és al costat (`alt=""`).
- Enllaços amb text significatiu (mai "clic aquí"); mida mínima de text 16px; respectar `prefers-color-scheme` i `prefers-reduced-motion`.
- Responsiu des de 320px sense scroll horitzontal.
- Idioma declarat (`<html lang="en">`).

## Llistat de decisions
| Data | Decisió | Motiu |
|---|---|---|
| 2026-11-20 | Web estàtica en HTML/CSS pla a GitHub Pages | Simplicitat i durabilitat |
| 2026-11-20 | Dades de persones a `data/people.json`; `people.html` generat | Una sola font de veritat, verificable |
| 2026-11-20 | Rebutjat l'estil "landing page" amb targetes | Sembla plantilla prefabricada |
| 2026-11-20 | Rebutjat text de meta-navegació a la Home | Farciment sense valor |
| 2026-11-20 | Eliminats "Human Motion Modeling" (TBA) i "HuPBA Seminar" (sense sessions) de la web | Principi 3: sense contingut real no es mostra; tornaran quan n'hi hagi |
| 2026-11-20 | Substituït el format serif acadèmic per un disseny modern: degradats, il·lustració pròpia, menú visible; descartades la landing tipus Stanford i la plantilla clàssica tipus Willow | Preferència de Xavier: modern i viu, però no landing amb menús amagats |
| 2026-11-20 | Pàgines generades des de `templates/` + `content/` | Una sola capçalera i peu; menys duplicació |
