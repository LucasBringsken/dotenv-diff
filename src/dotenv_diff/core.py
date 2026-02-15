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
            key, value, quoted = parse_env_line(line)
            if key:
                variable_map[key][str(path)] = (value, quoted)

    if len(variable_map) == 0:
        pprint("[yellow bold]No variables found in provided files.[/yellow bold]")
        raise typer.Exit(code=1)

    return variable_map


def strip_inline_comment(value: str) -> str:
    in_single = False
    in_double = False

    for i, char in enumerate(value):
        if char == "'" and not in_double:
            in_single = not in_single
        elif char == '"' and not in_single:
            in_double = not in_double
        elif char == "#" and not in_single and not in_double:
            if i == 0 or value[i - 1].isspace():
                return value[:i].rstrip()

    return value


def parse_env_line(line: str):
    line = line.strip()

    if not line or line.startswith("#"):
        return None, None, False

    if line.startswith("export "):
        line = line[7:].lstrip()

    if "=" not in line:
        return None, None, False

    key, value = line.split("=", 1)
    key = key.strip()
    value = strip_inline_comment(value.strip())

    quoted = False

    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        quoted = True
        value = value[1:-1]

    return key, value, quoted
