# A'Space adapter — gstack (référence du canonique)

**Adresse :** `fiber:a0:gstack` — D-N053 pas C (design Clara, design signé pas C D-C0..D-C3).
**Fork souverain :** `Amdkn/gstack` (parent `garrytan/gstack`, branche `main`).
**Gel amont :** `3742ee9527615b0fa325402d6c02498cc7fc19fa` (« feat: cut standalone /plan-eng-review; /autoplan keeps its eng phase (GST-1698) (#4108) »).
**Bind Cordis Fiber (4L) :** `a79170c7881ee66cc4068c3e5f9ee29abaf47fe9` — `aspace-plugin.json`, re-appliqué VERBATIM sur `main` au-dessus de l'adapter (F8 D4).
**Licence :** `MIT`.
**Version adapter :** 0.1.0 — contrat seul, patron pas A/B.

## Ce que fait l'adapter

gstack est une référence du canonique MasterSpec `fiber:a0:superpowers` (§D5) :
monorepo TypeScript (bun) — SKILL.md racine (routeur, généré depuis
SKILL.md.tmpl), 64 dossiers skills de premier niveau, `.gstack/`,
`agents/`, `autoplan/`, 1 745 fichiers `*.test.ts`.

Surface : `validate()` (constate : gel, licence, comptage des 64 skills,
80 SKILL.md, 1 745 tests, frontmatter du routeur, `.gstack/`/`agents/`/
`autoplan/`, présence du runner borné, zéro appel réseau), `doctor()`
(liste de contrôles), `describe()` (manifeste machine).
**Aucun fichier amont touché, aucun appel réseau, aucun poids monté dans le fork.**

Mesures au gel : 4 967 fichiers suivis, 64 skills premier niveau,
75 SKILL.md, 1 745 `*.test.ts`. Suite amont bornée (D-C2) :
`bun run scripts/test-free-shards.ts --quick` — sous-ensemble rapide défini
par l'amont (« explicit fast subset, not acceptance », honnête) ; suite
complète hors périmètre sur cette VM (sharding CI à 20 jobs).

Gel tenu : dérive 101, amont vivant — pas de re-gel, revisite par signal.

## Confinement

Aucun confinement commercial : code et skills MIT. Usage B2B autorisé par
la licence.

## Tests

```bash
python -m pytest aspace-gstack-adapter/tests/test_smoke.py -v
```

Suite amont bornée (bun 1.4.4, TMPDIR hors /tmp — /tmp tmpfs 512 Mo
saturé par les autres pistes) :

```bash
bun install
TMPDIR=$HOME/workspace/.tmp-pas-c bun run scripts/test-free-shards.ts --quick
```
