from __future__ import annotations

import argparse
import sys
from pathlib import Path

import nbformat


def _should_skip_black_isort(cell_source: str) -> bool:
    """
    Skip cells that likely contain IPython magics/shell escapes which Black cannot parse.
    """
    for line in cell_source.splitlines():
        stripped = line.lstrip()
        if stripped.startswith(("%", "!", "%%")):
            return True
    return False


def _format_python_source(source: str) -> tuple[str, bool]:
    """
    Returns (formatted_source, changed).
    """
    try:
        import black
        import isort
    except Exception as exc:  # pragma: no cover
        raise RuntimeError(
            "Missing formatter dependencies. Install `black` and `isort`."
        ) from exc

    sorted_source = isort.code(source, profile="black", line_length=88)

    mode = black.Mode(
        line_length=88,
        target_versions={black.TargetVersion.PY310},
    )
    try:
        formatted = black.format_file_contents(sorted_source, fast=False, mode=mode)
    except black.NothingChanged:
        formatted = sorted_source

    if source.endswith("\n") and not formatted.endswith("\n"):
        formatted += "\n"

    return formatted, formatted != source


def format_notebook(path: Path, *, write: bool) -> dict[str, int]:
    nb = nbformat.read(path, as_version=4)
    changed_cells = 0
    skipped_cells = 0
    errored_cells = 0

    for cell in nb.cells:
        if cell.get("cell_type") != "code":
            continue

        source = cell.get("source") or ""
        if not source.strip():
            continue

        if _should_skip_black_isort(source):
            skipped_cells += 1
            continue

        try:
            formatted, changed = _format_python_source(source)
        except Exception:
            errored_cells += 1
            continue

        if changed:
            cell["source"] = formatted
            changed_cells += 1

    if write and changed_cells:
        nbformat.write(nb, path)

    return {
        "changed_cells": changed_cells,
        "skipped_cells": skipped_cells,
        "errored_cells": errored_cells,
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Format .ipynb code cells with isort+black."
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Notebook files or directories (default: current dir).",
    )
    parser.add_argument(
        "--check", action="store_true", help="Only check; do not write."
    )
    args = parser.parse_args(argv)

    notebooks: list[Path] = []
    for raw in args.paths:
        p = Path(raw)
        if p.is_dir():
            notebooks.extend(sorted(p.rglob("*.ipynb")))
        elif p.is_file() and p.suffix.lower() == ".ipynb":
            notebooks.append(p)

    if not notebooks:
        print("No notebooks found.", file=sys.stderr)
        return 2

    write = not args.check
    any_changes_needed = False
    for nb_path in notebooks:
        stats = format_notebook(nb_path, write=write)
        if args.check and stats["changed_cells"]:
            any_changes_needed = True
        print(
            f"{nb_path}: changed={stats['changed_cells']} "
            f"skipped={stats['skipped_cells']} errored={stats['errored_cells']}"
        )

    return 1 if (args.check and any_changes_needed) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
