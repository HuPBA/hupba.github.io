# CLAUDE.md

@AGENTS.md

## Específic de Claude Code
- Les normes de treball són a `AGENTS.md` (importat a dalt) i les de disseny a `DESIGN.md`: llegeix-los abans de tocar res.
- Agents disponibles a `.claude/agents/`: `dissenyador-accessibilitat` (revisa disseny i accessibilitat) i `investigador` (recull i verifica dades de persones). Delega-hi quan la tasca els encaixi.
- Abans de donar una tasca per acabada, executa `python3 scripts/validate_people.py` i `python3 scripts/build_site.py --check`.
- No facis push ni creïs/modifiquis res a GitHub sense confirmació de l'usuari.
- Quan es prengui una decisió de disseny o de dades, deixa-la escrita a `DESIGN.md` o `AGENTS.md`; res no ha de dependre de l'historial de la sessió.
