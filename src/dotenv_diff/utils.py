from pathlib import Path
from rich import print as pprint
import typer


def expand_paths(raw_paths: list[Path]) -> list[Path]:
    expanded: list[Path] = []

    for path in raw_paths:
        if path.is_dir():
            expanded.extend(path.glob(".env*"))
            continue
        if "*" in path.name:
            expanded.extend(path.parent.glob(path.name))
            continue
        if path.exists():
            expanded.append(path)
        else:
            pprint(f"[red bold]File not found:[/red bold] {path}")
            raise typer.Exit(code=1)
    return expanded


def build_matrix_data(variable_map):
    keys = list(variable_map.keys())
    files = sorted({f for values in variable_map.values() for f in values})

    matrix = []
    for key in keys:
        row = [variable_map[key].get(f) for f in files]
        matrix.append((key, row))

    return files, matrix
