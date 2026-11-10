#!/usr/bin/env python3
"""Build one zip per skill in dist/, or check that the zips match the skill folders.

Each zip is named after its skill folder and holds that folder, so Claude can
install it with one upload:

    dist/search-console.zip
      search-console/
        SKILL.md

Both modes first check that every SKILL.md starts with valid YAML frontmatter
holding a name that matches its folder and a description, since Claude rejects
a skill whose frontmatter doesn't parse. This needs PyYAML (pip install pyyaml).

Usage:
    python3 scripts/build_zips.py          # rebuild every zip in dist/
    python3 scripts/build_zips.py --check  # fail if any zip is missing, stale or extra
"""

import io
import sys
import zipfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"
# A fixed timestamp keeps a rebuild of unchanged files byte-for-byte the same.
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def skill_files(skill_dir):
    return sorted(
        p for p in skill_dir.rglob("*")
        if p.is_file() and p.name != ".DS_Store"
    )


def frontmatter_problems(skill_dir):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    where = f"skills/{skill_dir.name}/SKILL.md"
    parts = text.split("---\n", 2)
    if not text.startswith("---\n") or len(parts) < 3:
        return [f"{where} has no frontmatter between --- lines"]
    try:
        data = yaml.safe_load(parts[1])
    except yaml.YAMLError as error:
        first_line = str(error).splitlines()[0]
        return [f"{where} frontmatter isn't valid YAML ({first_line}). Quote values that contain ': '"]
    if not isinstance(data, dict):
        return [f"{where} frontmatter isn't a set of keys"]
    problems = []
    if data.get("name") != skill_dir.name:
        problems.append(f"{where} name should be {skill_dir.name!r}")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        problems.append(f"{where} needs a description")
    return problems


def build_zip(skill_dir):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in skill_files(skill_dir):
            arcname = f"{skill_dir.name}/{path.relative_to(skill_dir).as_posix()}"
            info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            zf.writestr(info, path.read_bytes())
    return buffer.getvalue()


def contents(zip_bytes):
    """File names and bytes inside a zip, so the check doesn't depend on the zlib version."""
    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        return {name: zf.read(name) for name in zf.namelist()}


def main():
    check = "--check" in sys.argv[1:]
    bad = [problem for d in skill_dirs() for problem in frontmatter_problems(d)]
    if bad:
        print("Skill frontmatter problems:")
        for problem in bad:
            print(f"  - {problem}")
        return 1

    DIST.mkdir(exist_ok=True)
    expected = {f"{d.name}.zip": build_zip(d) for d in skill_dirs()}
    problems = []

    for name, data in expected.items():
        target = DIST / name
        if check:
            if not target.exists():
                problems.append(f"{name} is missing")
            elif contents(target.read_bytes()) != contents(data):
                problems.append(f"{name} doesn't match skills/{name[:-4]}/")
        else:
            target.write_bytes(data)

    for stale in sorted(DIST.glob("*.zip")):
        if stale.name not in expected:
            if check:
                problems.append(f"{stale.name} has no skill folder")
            else:
                stale.unlink()

    if problems:
        print("Skill zips are out of date:")
        for problem in problems:
            print(f"  - {problem}")
        print("Run `python3 scripts/build_zips.py` and commit dist/.")
        return 1

    print(f"{'Checked' if check else 'Built'} {len(expected)} skill zips in dist/.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
