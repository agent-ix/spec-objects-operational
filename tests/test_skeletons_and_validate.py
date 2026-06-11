"""Skeleton ↔ manifest-assert parity + quire roundtrip tests.

Each object type ships an authoring skeleton (``skeletons/<type>.md``) — a
complete worked example whose structure mirrors the manifest's
``body_extraction`` asserts. The locators here are ``frontmatter_field``,
``section_body``, and ``code_block`` (no tables / id patterns, unlike
spec-artifacts-iso). These tests cover:

* parity (regex-based, no quire import): every asserted heading exists at the
  asserted level, every asserted ``code_block`` carries the asserted fence
  language, the skeleton does not drift ahead of the contract (reverse
  direction), required ``section_body`` sections are substantive and
  placeholder-free, and the frontmatter carries every required
  ``frontmatter_field`` with ``artifact_type`` equal to the type name;
* roundtrip: each skeleton passes ``quire.validate_document`` and a mutated
  copy fails (requires a quire wheel exposing the markdown validator; skipped
  cleanly otherwise — quire is intentionally NOT a dependency).
"""

from __future__ import annotations

import pathlib
import re

import pytest
import yaml

PKG_ROOT = pathlib.Path(__file__).resolve().parent.parent / "spec_objects_operational"
MANIFEST_PATH = PKG_ROOT / "manifest.yaml"
SKELETONS_DIR = PKG_ROOT / "skeletons"

OBJECT_TYPE_NAMES = [
    "configuration",
    "migration",
    "sli",
    "slo",
    "alert",
    "runbook",
    "incident",
    "deployment",
]

_PLACEHOLDER_TOKENS = ("TODO", "TBD", "{{", "}}", "placeholder", "none specified")

# section_body / code_block locators carry no explicit level facet; the
# convention (and every skeleton) addresses H2 headings.
_HEADING_LEVEL = 2


def _object_types() -> list[dict]:
    return yaml.safe_load(MANIFEST_PATH.read_text()).get("object_types", [])


def _object_type(name: str) -> dict:
    return next(ot for ot in _object_types() if ot["name"] == name)


def _locators(ot: dict) -> dict[str, dict]:
    be = ot.get("body_extraction") or {}
    return (be.get("yield_pattern") or {}).get("match") or {}


def _skeleton_text(name: str) -> str:
    return (SKELETONS_DIR / f"{name}.md").read_text()


def _frontmatter(markdown: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", markdown, re.DOTALL)
    assert m, "skeleton missing frontmatter"
    return yaml.safe_load(m.group(1))


def _strip_frontmatter(markdown: str) -> str:
    return re.sub(r"^---\n.*?\n---\n", "", markdown, count=1, flags=re.DOTALL)


def _skeleton_headings(markdown: str) -> list[tuple[int, str]]:
    """Return ``[(level, text)]`` for every ATX heading outside code fences."""
    body = _strip_frontmatter(markdown)
    out: list[tuple[int, str]] = []
    in_fence = False
    for line in body.splitlines():
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r"^(#{1,6})\s+(.*\S)\s*$", line)
        if m:
            out.append((len(m.group(1)), m.group(2).strip()))
    return out


def _split_sections(markdown: str, level: int = _HEADING_LEVEL) -> dict[str, str]:
    """Return ``{section_name: body_text}`` for headings at the given level."""
    body = _strip_frontmatter(markdown)
    sections: dict[str, str] = {}
    current: str | None = None
    buf: list[str] = []
    prefix = "#" * level + " "
    for line in body.splitlines():
        if line.startswith(prefix) and not line[level + 1 :].startswith("#"):
            if current is not None:
                sections[current] = "\n".join(buf).strip()
            current = line[len(prefix) :].strip()
            buf = []
        elif current is not None:
            buf.append(line)
    if current is not None:
        sections[current] = "\n".join(buf).strip()
    return sections


def _fence_languages(section_body: str) -> list[str]:
    """Return the info string of every opening code fence in a section body."""
    out: list[str] = []
    in_fence = False
    for line in section_body.splitlines():
        if line.startswith("```"):
            if not in_fence:
                out.append(line[3:].strip())
            in_fence = not in_fence
    return out


# ─── Manifest sanity ──────────────────────────────────────────────────────


def test_manifest_declares_exactly_the_expected_object_types() -> None:
    assert [ot["name"] for ot in _object_types()] == OBJECT_TYPE_NAMES


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_core_frontmatter_locators_are_required(name: str) -> None:
    """id / title / artifact_type are required in BOTH anchor groups."""
    locators = _locators(_object_type(name))
    for field in ("id", "title", "artifact_type"):
        loc = locators[field]
        assert loc["from"] == "frontmatter_field", f"{name}.{field}"
        assert loc["required"] is True, f"{name}.{field} is not required"


_REQUIRED_DEFINING_FIELDS = {
    "configuration": ["parameters"],
    "migration": ["sql"],
    "sli": ["query"],
    "slo": ["target", "window"],
    "alert": ["flow"],
    "runbook": ["steps"],
    "incident": ["timeline"],
    "deployment": ["topology"],
}


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_defining_fields_are_required(name: str) -> None:
    locators = _locators(_object_type(name))
    for field in _REQUIRED_DEFINING_FIELDS[name]:
        assert locators[field]["required"] is True, f"{name}.{field} not required"


# ─── Skeleton presence + frontmatter parity ───────────────────────────────


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_skeleton_exists(name: str) -> None:
    assert (SKELETONS_DIR / f"{name}.md").exists(), f"missing skeleton {name}.md"


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_skeleton_frontmatter_carries_required_fields(name: str) -> None:
    """Every required frontmatter_field locator is satisfied by the skeleton,
    and ``artifact_type`` equals the object-type name."""
    fm = _frontmatter(_skeleton_text(name))
    locators = _locators(_object_type(name))
    for field, loc in locators.items():
        if loc.get("from") != "frontmatter_field" or not loc.get("required"):
            continue
        path = loc["path"]
        assert len(path) == 1, f"{name}.{field}: unexpected nested path {path}"
        value = fm.get(path[0])
        assert value not in (None, ""), f"{name}: frontmatter missing {path[0]!r}"
    assert fm["artifact_type"] == name


# ─── Forward parity: asserted structure exists in the skeleton ────────────


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_asserted_headings_exist_at_asserted_level(name: str) -> None:
    """Every section_body / code_block locator's heading exists as an H2."""
    md = _skeleton_text(name)
    headings = set(_skeleton_headings(md))
    for field, loc in _locators(_object_type(name)).items():
        if loc.get("from") not in ("section_body", "code_block"):
            continue
        wanted = (_HEADING_LEVEL, loc["after_heading"])
        assert wanted in headings, (
            f"{name}: locator {field!r} expects heading "
            f"{'#' * wanted[0]} {wanted[1]} which is absent from the skeleton"
        )


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_asserted_code_blocks_carry_asserted_language(name: str) -> None:
    """Every code_block locator finds a fence under its heading whose info
    string matches the asserted language (any fence when none is asserted)."""
    md = _skeleton_text(name)
    sections = _split_sections(md)
    for field, loc in _locators(_object_type(name)).items():
        if loc.get("from") != "code_block":
            continue
        section = sections.get(loc["after_heading"])
        assert section, f"{name}: no body under heading {loc['after_heading']!r}"
        langs = _fence_languages(section)
        assert langs, f"{name}: locator {field!r} found no code fence"
        wanted = loc.get("language")
        if wanted is not None:
            assert wanted in langs, (
                f"{name}: locator {field!r} asserts language {wanted!r} "
                f"but skeleton fences carry {langs}"
            )


# ─── Reverse parity: the skeleton does not drift ahead of the contract ────


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_skeleton_headings_do_not_drift_from_asserts(name: str) -> None:
    """Every H2 heading in the skeleton is addressed by some locator, so the
    skeleton cannot drift ahead of the manifest contract."""
    asserted = {
        loc["after_heading"]
        for loc in _locators(_object_type(name)).values()
        if loc.get("from") in ("section_body", "code_block")
    }
    for level, text in _skeleton_headings(_skeleton_text(name)):
        if level != _HEADING_LEVEL:
            continue
        assert text in asserted, (
            f"{name}: skeleton heading {text!r} (H{level}) is not asserted "
            f"by the manifest (skeleton drifted ahead of the contract)"
        )


# ─── Substantive, placeholder-free bodies ─────────────────────────────────


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_required_section_bodies_are_substantive(name: str) -> None:
    md = _skeleton_text(name)
    sections = _split_sections(md)
    for field, loc in _locators(_object_type(name)).items():
        if loc.get("from") not in ("section_body", "code_block"):
            continue
        if not loc.get("required"):
            continue
        heading = loc["after_heading"]
        assert heading in sections, f"{name}: section {heading!r} missing"
        body = sections[heading]
        assert body, f"{name}: section {heading!r} is empty in skeleton"
        lowered = body.lower()
        for token in _PLACEHOLDER_TOKENS:
            assert (
                token.lower() not in lowered
            ), f"{name}: section {heading!r} carries placeholder token {token!r}"


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_skeleton_body_is_placeholder_free(name: str) -> None:
    """The whole body (frontmatter stripped) is free of placeholder tokens."""
    body = _strip_frontmatter(_skeleton_text(name)).lower()
    for token in _PLACEHOLDER_TOKENS:
        assert (
            token.lower() not in body
        ), f"{name}: skeleton carries placeholder token {token!r}"


# ─── Roundtrip via the quire Python wheel (guarded) ───────────────────────


def _quire_doc_validator():
    """Return the quire wheel iff it exposes the markdown validator."""
    try:
        import quire
    except ImportError:
        return None
    if not hasattr(quire, "validate_document"):
        return None
    return quire


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_skeleton_validates_via_quire(name: str) -> None:
    """Each filled skeleton passes validate_document.

    Skips when no quire wheel (or one predating the markdown validator) is
    installed; quire is intentionally not a dependency of this package."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    res = quire.validate_document(name, str(PKG_ROOT), _skeleton_text(name))
    assert res["is_valid"], res["errors"]


@pytest.mark.parametrize("name", OBJECT_TYPE_NAMES)
def test_mutated_skeleton_fails_validation(name: str) -> None:
    """Deleting the defining required section/field makes validation fail."""
    quire = _quire_doc_validator()
    if quire is None:
        pytest.skip("quire wheel lacks validate_document")
    base = _skeleton_text(name)
    if name == "slo":
        mutated = re.sub(r"^target:.*\n", "", base, count=1, flags=re.MULTILINE)
    else:
        loc = _locators(_object_type(name))[_REQUIRED_DEFINING_FIELDS[name][0]]
        heading = f"## {loc['after_heading']}"
        mutated = re.sub(
            rf"^{re.escape(heading)}$.*?(?=^## |\Z)",
            "",
            base,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
    assert mutated != base, f"{name}: mutation did not apply"
    res = quire.validate_document(name, str(PKG_ROOT), mutated)
    assert not res["is_valid"], f"{name}: mutated skeleton still validates"
