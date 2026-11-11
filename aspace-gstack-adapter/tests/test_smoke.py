"""Smoke tests de l'adapter gstack (D-N053 pas C).

Roulés avec le venv du pas : `python -m pytest aspace-gstack-adapter/tests/test_smoke.py -v`.
Ne touchent pas l'amont, ne font aucun appel réseau. La validation complète
de la suite est celle de la suite amont bornée (`bun run
scripts/test-free-shards.ts --quick`, sous-ensemble rapide défini par
l'amont, « not acceptance ») ; le smoke vérifie les constantes, les
comptages mesurés par l'adapter et le statut de référence du canonique (§D5).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import aspace_gstack_adapter as adapter  # noqa: E402


def test_constants():
    assert re.fullmatch(r"[0-9a-f]{40}", adapter.PINNED_UPSTREAM_COMMIT)
    assert adapter.FIBER_ADDRESS == "fiber:a0:gstack"
    assert adapter.LICENSE == "MIT"
    assert adapter.FORK == "Amdkn/gstack"
    assert adapter.UPSTREAM_REPO == "garrytan/gstack"
    assert adapter.ADAPTER_VERSION == "0.1.0"
    assert adapter.BIND_COMMIT == "a79170c7881ee66cc4068c3e5f9ee29abaf47fe9"
    assert adapter.BIND_LAYER == "4L"


def test_validate_counts():
    v = adapter.validate()
    assert v["pinned_commit_is_40_hex"] is True
    assert v["license_file_present"] is True
    assert v["skill_dirs_top_level"] == 64
    assert v["skill_md_total_on_disk"] == 75
    assert v["test_ts_total_on_disk"] == 1745
    assert v["root_skill_md_present"] is True
    assert v["root_skill_frontmatter_ok"] is True
    assert v["gstack_expected_missing"] == []
    assert v["agents_present"] is True
    assert v["agents_openai_yaml"] is True
    assert v["autoplan_present"] is True
    assert v["autoplan_skill_md"] is True
    assert v["autoplan_driver_md"] is True
    assert v["quick_runner_present"] is True
    assert v["adapter_network_calls"] == 0
    assert v["confinement"]


def test_validate_coherent():
    v = adapter.validate()
    assert v["inventory_coherent"] is True
    assert v["canonical"] == "fiber:a0:superpowers"


def test_doctor_all_pass():
    checks = adapter.doctor()
    assert checks, "doctor() vide"
    failed = [c for c in checks if not c["ok"]]
    assert not failed, failed


def test_no_network_import_in_adapter():
    src = (Path(adapter.__file__).parent / "__init__.py").read_text()
    for banned in ("requests", "httpx", "urllib", "socket", "huggingface_hub", "aiohttp"):
        assert banned not in src, banned


def test_describe():
    d = adapter.describe()
    assert d["fiber"] == "fiber:a0:gstack"
    assert d["pinned_upstream_commit"] == adapter.PINNED_UPSTREAM_COMMIT
    assert d["license"] == "MIT"
    assert d["canonical"] == "fiber:a0:superpowers"
