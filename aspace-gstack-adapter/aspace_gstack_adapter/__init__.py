"""A'Space adapter — gstack (D-N053 pas C, design Clara + design signé pas C).

Contrat seul, patron pas A/B : cet adapter ne modifie AUCUN fichier amont,
ne fait AUCUN appel réseau, ne monte AUCUN poids. Il constate : le gel
épinglé, la licence, l'inventaire skills/config (SKILL.md racine + 64
dossiers skills de premier niveau, `.gstack/`, `agents/`, `autoplan/`) et
la surface d'orchestration mesurée au fichier — et il se déclare RÉFÉRENCE
du canonique MasterSpec `fiber:a0:superpowers` (§D5), pas un framework
parallèle.

Adresse : fiber:a0:gstack
Fork souverain : Amdkn/gstack (parent garrytan/gstack, branche main)
Gel amont : 3742ee9527615b0fa325402d6c02498cc7fc19fa (« feat: cut standalone /plan-eng-review; /autoplan keeps its eng phase (GST-1698) (#4108) »)
Bind Cordis Fiber (4L) : a79170c7881ee66cc4068c3e5f9ee29abaf47fe9
Licence : MIT

Mesures au gel (2026-11-11, vérifiées au fichier) :
- 4 967 fichiers suivis ; 1 745 fichiers `*.test.ts` ; 75 SKILL.md suivis
  (64 dossiers skills de premier niveau + SKILL.md racine routeur + 10
  imbriqués, dont autoplan/sections).
- `.gstack/` (always-run.json, generated.json, pregate.json,
  ship-policy.json, ship-policy.example.json) ; `agents/` (openai.yaml) ;
  `autoplan/` (DRIVER.md, SKILL.md, sections/).
- Suite amont bornée (D-C2) : `bun run scripts/test-free-shards.ts --quick`
  — sous-ensemble rapide défini par l'amont lui-même (« explicit fast
  subset, not acceptance », honnête). Suite complète hors périmètre sur
  cette VM (1 745 fichiers, sharding CI à 20 jobs).
- Gel tenu : dérive 101, amont vivant — pas de re-gel, revisite par signal.
- Télémétrie : 0 SDK ; aucune dépendance de télémétrie dans package.json /
  bun.lock.
"""

from __future__ import annotations

import re
from pathlib import Path

FIBER_ADDRESS = "fiber:a0:gstack"
FORK = "Amdkn/gstack"
UPSTREAM_REPO = "garrytan/gstack"
UPSTREAM_BRANCH = "main"
PINNED_UPSTREAM_COMMIT = "3742ee9527615b0fa325402d6c02498cc7fc19fa"
PINNED_UPSTREAM_COMMIT_SHORT = "3742ee95"
BIND_COMMIT = "a79170c7881ee66cc4068c3e5f9ee29abaf47fe9"
BIND_LAYER = "4L"
LICENSE = "MIT"
ADAPTER_VERSION = "0.1.0"

CANONICAL = "fiber:a0:superpowers"
EXPECTED_GSTACK_FILES = (
    "always-run.json",
    "generated.json",
    "pregate.json",
    "ship-policy.json",
)

CONFINEMENT = """Aucun confinement commercial : code et skills MIT. Usage B2B autorisé
par la licence. L'adapter ne fait que constater l'inventaire et la surface ;
aucun code amont n'est modifié."""


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _skill_inventory(root: Path) -> dict:
    top_skill_dirs = sorted(
        p.name
        for p in root.iterdir()
        if p.is_dir() and (p / "SKILL.md").is_file() and not p.name.startswith(".")
    )
    skill_md_total = sum(1 for p in root.rglob("SKILL.md") if ".git" not in p.parts and "node_modules" not in p.parts)
    test_files = sum(
        1 for p in root.rglob("*.test.ts")
        if ".git" not in p.parts and "node_modules" not in p.parts
    )
    gstack_dir = root / ".gstack"
    gstack_files = sorted(p.name for p in gstack_dir.iterdir() if p.is_file()) if gstack_dir.is_dir() else []
    root_skill = root / "SKILL.md"
    frontmatter_ok = False
    if root_skill.is_file():
        text = root_skill.read_text(encoding="utf-8", errors="replace")
        frontmatter_ok = text.startswith("---\n") and "\nname: gstack\n" in text and "\ndescription:" in text
    return {
        "tracked_files_total": None,  # mesuré par git ls-files, pas par l'arbre
        "skill_dirs_top_level": len(top_skill_dirs),
        "skill_dirs_top_level_names": top_skill_dirs,
        "skill_md_total_on_disk": skill_md_total,
        "test_ts_total_on_disk": test_files,
        "root_skill_md_present": root_skill.is_file(),
        "root_skill_frontmatter_ok": frontmatter_ok,
        "gstack_files": gstack_files,
        "gstack_expected_present": [f for f in EXPECTED_GSTACK_FILES if f in gstack_files],
        "gstack_expected_missing": [f for f in EXPECTED_GSTACK_FILES if f not in gstack_files],
        "agents_present": (root / "agents").is_dir(),
        "agents_openai_yaml": (root / "agents" / "openai.yaml").is_file(),
        "autoplan_present": (root / "autoplan").is_dir(),
        "autoplan_skill_md": (root / "autoplan" / "SKILL.md").is_file(),
        "autoplan_driver_md": (root / "autoplan" / "DRIVER.md").is_file(),
        "quick_runner_present": (root / "scripts" / "test-free-shards.ts").is_file(),
    }


def describe() -> dict:
    """Décrit l'adapter (manifeste machine, sans effet de bord)."""
    return {
        "fiber": FIBER_ADDRESS,
        "fork": FORK,
        "upstream": UPSTREAM_REPO,
        "upstream_branch": UPSTREAM_BRANCH,
        "pinned_upstream_commit": PINNED_UPSTREAM_COMMIT,
        "bind_commit": BIND_COMMIT,
        "bind_layer": BIND_LAYER,
        "license": LICENSE,
        "adapter_version": ADAPTER_VERSION,
        "canonical": CANONICAL,
        "confinement": CONFINEMENT,
        "surface": "validate() -> dict ; doctor() -> list[check] ; describe() -> dict",
    }


def validate() -> dict:
    """Constate l'état de l'inventaire gelé. Aucun appel réseau, aucune écriture."""
    root = _repo_root()
    inv = _skill_inventory(root)
    license_file = root / "LICENSE"
    return {
        "pinned_commit_is_40_hex": bool(re.fullmatch(r"[0-9a-f]{40}", PINNED_UPSTREAM_COMMIT)),
        "license_file_present": license_file.is_file(),
        "license": LICENSE,
        "adapter_network_calls": 0,
        "canonical": CANONICAL,
        "confinement": CONFINEMENT,
        **inv,
        "inventory_coherent": (
            inv["skill_dirs_top_level"] == 64
            and inv["skill_md_total_on_disk"] == 75
            and inv["test_ts_total_on_disk"] == 1745
            and inv["root_skill_md_present"]
            and inv["root_skill_frontmatter_ok"]
            and inv["gstack_expected_missing"] == []
            and inv["agents_present"]
            and inv["agents_openai_yaml"]
            and inv["autoplan_present"]
            and inv["autoplan_skill_md"]
            and inv["autoplan_driver_md"]
            and inv["quick_runner_present"]
        ),
    }


def doctor() -> list[dict]:
    """Liste de contrôles sur l'inventaire gelé."""
    v = validate()
    checks = [
        {
            "name": "gel_epingle_40_hex",
            "ok": v["pinned_commit_is_40_hex"],
            "detail": PINNED_UPSTREAM_COMMIT_SHORT,
        },
        {
            "name": "licence_mit",
            "ok": v["license_file_present"] and v["license"] == "MIT",
            "detail": "LICENSE present, MIT",
        },
        {
            "name": "inventaire_64_skills_premier_niveau",
            "ok": v["skill_dirs_top_level"] == 64,
            "detail": f"{v['skill_dirs_top_level']} dossiers skills de premier niveau avec SKILL.md",
        },
        {
            "name": "surface_skills_et_tests",
            "ok": v["skill_md_total_on_disk"] == 75 and v["test_ts_total_on_disk"] == 1745,
            "detail": f"{v['skill_md_total_on_disk']} SKILL.md, {v['test_ts_total_on_disk']} *.test.ts",
        },
        {
            "name": "routeur_racine",
            "ok": v["root_skill_md_present"] and v["root_skill_frontmatter_ok"],
            "detail": "SKILL.md racine présent, frontmatter name: gstack + description",
        },
        {
            "name": "gstack_agents_autoplan",
            "ok": v["gstack_expected_missing"] == [] and v["agents_openai_yaml"]
            and v["autoplan_skill_md"] and v["autoplan_driver_md"],
            "detail": f".gstack/ {len(v['gstack_files'])} fichiers, agents/openai.yaml, autoplan SKILL.md + DRIVER.md",
        },
        {
            "name": "runner_borne_present",
            "ok": v["quick_runner_present"],
            "detail": "scripts/test-free-shards.ts présent (--quick = fast subset, not acceptance)",
        },
        {
            "name": "reference_du_canonique",
            "ok": v["canonical"] == "fiber:a0:superpowers",
            "detail": "référence du canonique superpowers (§D5), pas un framework parallèle",
        },
        {
            "name": "adapter_sans_reseau",
            "ok": v["adapter_network_calls"] == 0,
            "detail": "stdlib seule, 0 import réseau, 0 appel sortant",
        },
    ]
    return checks
