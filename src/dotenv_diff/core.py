from collections import defaultdict
from pathlib import Path
from rich import print as pprint
import typer


def compare(file_paths: list[Path]) -> defaultdict:
    variable_map = defaultdict(dict)
    for path in file_paths:
        file_content = path.read_text()
        file_lines = file_content.splitlines()

        for line in file_lines:
            if not line.strip() or "=" not in line:
                continue

            key, value = line.split("=", 1)
            variable_map[key.strip()][str(path)] = value.strip()

    if len(variable_map) == 0:
        pprint("[yellow bold]No variables found in provided files.[/yellow bold]")
        raise typer.Exit(code=1)

    return variable_map
