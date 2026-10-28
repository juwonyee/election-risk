# AGENTS.md

Guidelines for agents working **on** this repository. Installing it instead? See the README.

## What lives where

- `skills/` is the product: four Agent Skills (`profit-structure`, `candidate-positions`,
  `prediction-markets`, `election-risk`), each with `SKILL.md`, `references/`, `agents/openai.yaml`,
  `LICENSE`, and `scripts/` with a copy of the engine so each works when installed alone. `election-risk`
  calls the others by name (`$profit-structure`); they hand off through files in `election-risk-out/`.
- `engine/` is the source of truth for the Python engine (`erisk.py` + `erisk_engine/`). Never edit any
  `skills/*/scripts/` directly: edit `engine/`, then run `python3 scripts/sync_engine.py`.
- The policy book (candidate positions) is never committed. Users build it, or download the maintainers'
  copy from a release with `erisk book download --accept-risk`.
- `examples/` holds worked company folders (the same layout the engine writes to `election-risk-out/`).
- `research/` is development material (company notes, market catalogs). It is not installed.
- `.claude-plugin/`, `.codex-plugin/`, `.cursor-plugin/`, `.agents/plugins/`, `gemini-extension.json` make
  the repo installable as one plugin.

## Checks before a change ships

```bash
python3 scripts/sync_engine.py --check     # the skill's engine copy matches engine/
python3 scripts/validate_skills.py         # spec: name = folder, description <= 1024 chars, links resolve
python3 -m unittest discover tests         # offline engine tests
```

## Rules for skill content

- Frontmatter uses only spec fields (`name`, `description`, `license`, `compatibility`, `metadata`,
  `allowed-tools`) so skills also load on claude.ai and the API.
- Descriptions: third person, what it does + when to use it.
- Keep SKILL.md short (it loads on every use); detail goes in `references/`, linked one level deep with a note
  on when to read it. Time-sensitive context lives only in `skills/election-risk/references/policy.md`. The probability
  table (`skills/candidate-positions/references/probability-table.md`) changes only with new research in
  `research/probability-table/`.
- Never add buy/sell language, position sizing, or anything that helps get around a venue's geo-restrictions.

## Versioning

`VERSION`, both plugin manifests and the marketplace files share one x.y.z: x = restructure, y = new skill,
z = changes to existing skills. Bump `metadata.version` in any SKILL.md you change.
