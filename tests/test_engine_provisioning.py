"""Engine-provisioning policy tests (FR-005-AC-10, FR-005-AC-11).

The semantic rows of this suite are only worth reading if they cannot pass
without the engine. That policy lives in `conftest.require_quire`, and these
two tests are what stop it from silently becoming a skip again.
"""

from __future__ import annotations

import builtins
import sys

import pytest

from tests import conftest
from tests.conftest import REPO_ROOT, require_quire


@pytest.mark.trace("TC-071", "FR-005-AC-10")
def test_a_missing_engine_fails_the_semantic_rows_and_names_the_provisioning_path(
    monkeypatch,
):
    """FR-005-AC-10: with the wheel absent every semantic row FAILS. A skip
    would be reported green, and a green row over an absent engine is not
    coverage."""
    real_import = builtins.__import__

    def refuse_quire(name, *args, **kwargs):
        if name == "quire":
            raise ImportError("No module named 'quire'")
        return real_import(name, *args, **kwargs)

    monkeypatch.delitem(sys.modules, "quire", raising=False)
    monkeypatch.setattr(builtins, "__import__", refuse_quire)
    with pytest.raises(BaseException) as raised:
        require_quire()
    # `pytest.fail` raises Failed; a skip would raise Skipped. That
    # distinction is the whole point of the policy.
    assert isinstance(raised.value, pytest.fail.Exception), raised.value
    assert not isinstance(raised.value, pytest.skip.Exception), raised.value
    message = str(raised.value)
    assert "extract_semantic" in message
    assert "poetry install" in message


@pytest.mark.trace("TC-071", "FR-005-AC-10")
def test_an_engine_without_extract_semantic_fails_the_same_way(monkeypatch):
    class Stub:
        pass

    monkeypatch.setitem(sys.modules, "quire", Stub())
    with pytest.raises(BaseException) as raised:
        require_quire()
    assert isinstance(raised.value, pytest.fail.Exception), raised.value
    assert not isinstance(raised.value, pytest.skip.Exception), raised.value
    assert "extract_semantic" in str(raised.value)
    assert "poetry install" in str(raised.value)


@pytest.mark.trace("TC-072", "FR-005-AC-11")
def test_quire_is_declared_as_a_dev_dependency_from_internal_pypi():
    """FR-005-AC-11: `quire` is a committed dev dependency pinned to the
    `internal-pypi` source, so `poetry install` provisions the engine and no
    lookup falls through to public PyPI, where `quire` names an unrelated
    package. No `dev-quire` target remains anywhere in the repo."""
    import tomlkit

    config = tomlkit.parse((REPO_ROOT / "pyproject.toml").read_text())
    poetry = config["tool"]["poetry"]
    dev = poetry["group"]["dev"]["dependencies"]
    assert dev["quire"]["source"] == "internal-pypi"

    assert "dev-quire" not in config["tool"]["poe"]["tasks"]

    makefile = (REPO_ROOT / "Makefile").read_text()
    assert "dev-quire" not in makefile
    assert "quire-rs#392" not in makefile

    # The policy text the failure message quotes lives in one place.
    assert "poetry install" in conftest.QUIRE_MISSING
