from collections import defaultdict
from pandas import DataFrame
from pathlib import Path
from rich import print as pprint
from rich import box
from rich.table import Table
from rich.console import Console, Group
from rich.rule import Rule
from rich.panel import Panel
import typer
from typing import List


console = Console()


app = typer.Typer(
    help="Handy tool for quickly spotting missing keys and differing values in .env files",
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def _app_callback(
    ctx: typer.Context,
    reveal: bool = typer.Option(False, "--reveal", help="Reveals masked values."),
):
    if ctx.obj is None:
        ctx.obj = {}
    ctx.obj["reveal"] = reveal


@app.command()
def summary(
    file_paths: List[Path] = typer.Argument(..., help="Paths to .env files"),
):
    """Show a diff summary for the provided files."""
    file_paths = expand_paths(list(file_paths))
    variable_map = compare(file_paths)
    print_summary(variable_map)


@app.command()
def values(
    file_paths: List[Path] = typer.Argument(..., help="Paths to .env files"),
):
    """Show value diffs as a matrix."""
    file_paths = expand_paths(list(file_paths))
    variable_map = compare(file_paths)
    print_value_matrix(variable_map)


@app.command()
def presence(
    file_paths: List[Path] = typer.Argument(..., help="Paths to .env files"),
):
    """Show presence diffs as a matrix."""
    file_paths = expand_paths(list(file_paths))
    variable_map = compare(file_paths)
    print_presence_matrix(variable_map)


def print_summary(map: dict):
    df = DataFrame.from_dict(map, orient="index")
    num_files = len(df.columns)
    num_vars = len(df.index)

    incomplete_mask = df.isna().any(axis=1)
    diverging_mask = df.nunique(axis=1) > 1

    missing_count = int(incomplete_mask.sum())
    modified_count = int(diverging_mask.sum())

    summary_content = Group(
        "[bold cyan]SUMMARY[/bold cyan]",
        Rule(style="bright_black"),
        f"[bold]Total Files:[/bold]         [green]{num_files}[/green]",
        f"[bold]Unique Keys:[/bold]         [blue]{num_vars}[/blue]",
        f"[bold]Incomplete Keys:[/bold]     [red]{missing_count}[/red]",
        f"[bold]Diverging Values:[/bold]    [yellow]{modified_count}[/yellow]",
    )
    console.print(
        Panel(
            summary_content, expand=False, border_style="bright_black", padding=(1, 2)
        )
    )

    if missing_count > 0:
        incomplete_details = []
        for key, row in df[incomplete_mask].iterrows():
            missing_in = row.index[row.isna()].tolist()

            incomplete_details.append(f"• [bold red]{key}[/bold red] is missing in:")

            for file in missing_in:
                incomplete_details.append(f"  [dim]↳ {file}[/dim]")

            incomplete_details.append("")

        console.print(
            Panel(
                Group(*incomplete_details[:-1]),
                title="[red]Incomplete Key Details[/red]",
                title_align="left",
                border_style="red",
                padding=(1, 2),
            )
        )

    if modified_count > 0:
        diverging_details = []
        for key, row in df[diverging_mask].iterrows():
            values = row.dropna()

            diverging_details.append(f"• [bold yellow]{key}[/bold yellow]")

            for file, val in values.items():
                diverging_details.append(f"  [dim]↳ {file}:[/dim] [cyan]{val}[/cyan]")

            diverging_details.append("")

        console.print(
            Panel(
                Group(*diverging_details),
                title="[yellow]Diverging Value Details[/yellow]",
                title_align="left",
                border_style="yellow",
                padding=(1, 2),
            )
        )


def print_value_matrix(map: dict):
    df, table = build_matrix(map)

    for idx, row in df.iterrows():
        table.add_row(
            str(idx),
            *[str(v) if v == v else "[red bold]—[/red bold]" for v in row],
        )

    console.print(table)


def print_presence_matrix(map: dict):
    df, table = build_matrix(map, center_values=True)

    for idx, row in df.iterrows():
        table.add_row(str(idx), *["✅" if v == v else "❌" for v in row])

    console.print(table)


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


def build_matrix(map: dict, center_values: bool = False) -> tuple[DataFrame, Table]:
    df = DataFrame.from_dict(map, orient="index")

    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
        border_style="bright_black",
    )
    table.add_column("VARIABLE", style="bold")

    for col in df.columns:
        table.add_column(
            col, style="cyan", justify="center" if center_values else "default"
        )

    return (df, table)
