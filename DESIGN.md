# DESIGN.md — decisions de disseny

Registre viu. Cada decisió: què, per què. Si canvia, s'edita aquí i s'indica la data.

## Principis
1. **Contingut primer.** Una web de grup de recerca serveix per trobar gent, línies de recerca, projectes i publicacions. Cap element decoratiu que no ajudi a això.
2. **Sembla una web acadèmica, no una plantilla de màrqueting.** Res de hero gegant, targetes, gradients, icones decoratives ni crides a l'acció (*decisió de Xavier, 2026-11-20: la primera versió "landing" es va rebutjar*).
3. **Sense text de farciment ni meta-navegació.** Prohibits textos com "See the people, our research…", "Welcome to…", "coming soon" o "upcoming sessions will be announced here". Si una secció no té contingut real, **no existeix** (ni es mostra enllaç).
4. **Tot el que es mostra és verificable** (vegeu `AGENTS.md`, secció Persones).
5. **Lleuger i durable**: HTML i CSS pla, sense frameworks ni dependències d'execució; ha de funcionar sense JavaScript.

## Estat actual (provisional, 2026-11-20)
Pàgines: Home, People, Research, Projects, Events. Tipografia serif de sistema (Charter/Georgia), una columna estreta (46rem), enllaços granats, menú de text, mode fosc automàtic. La Home és només la descripció del grup. **Pendent de redefinir "des de la base"** amb l'usuari: estructura de pàgines, jerarquia i to.

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
