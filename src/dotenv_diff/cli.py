from pathlib import Path
from .core import compare
from .utils import expand_paths
from .output import print_summary, print_value_matrix, print_presence_matrix
import typer
from typing import List

app = typer.Typer(
    help="Lightweight tool for quickly spotting missing keys and differing values in .env files",
    add_completion=False,
)


@app.callback(invoke_without_command=True)
def _app_callback(
    ctx: typer.Context,
):
    if ctx.obj is None:
        ctx.obj = {}

    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit(code=1)


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
