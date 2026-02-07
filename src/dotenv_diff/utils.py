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
