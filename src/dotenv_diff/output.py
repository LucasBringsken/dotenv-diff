from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich import box
from .utils import build_matrix_data, mask_value

console = Console()


def print_summary(variable_map: dict, reveal: bool = False):
    files, rows = build_matrix_data(variable_map)

    num_files = len(files)
    num_vars = len(rows)

    missing_count = sum(any(v is None for v in values) for _, values in rows)

    modified_count = sum(
        len({v[0] for v in values if v is not None}) > 1 for _, values in rows
    )

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
        for key, values in rows:
            missing_in = [files[i] for i, v in enumerate(values) if v is None]
            if not missing_in:
                continue

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

        for key, values in rows:
            present = {files[i]: v for i, v in enumerate(values) if v is not None}

            if len(set(present.values())) <= 1:
                continue

            diverging_details.append(f"• [bold yellow]{key}[/bold yellow]")

            for file, val in present.items():
                diverging_details.append(
                    f"  [dim]↳ {file}:[/dim] [cyan]{mask_value(val, reveal)}[/cyan]"
                )

            diverging_details.append("")

        console.print(
            Panel(
                Group(*diverging_details[:-1]),
                title="[yellow]Diverging Value Details[/yellow]",
                title_align="left",
                border_style="yellow",
                padding=(1, 2),
            )
        )


def print_value_matrix(variable_map: dict, reveal: bool = False):
    files, rows = build_matrix_data(variable_map)
    table = build_table(files)

    for key, row in rows:
        table.add_row(
            key,
            *[
                (
                    str(mask_value(v, reveal))
                    if v is not None
                    else "[red bold]—[/red bold]"
                )
                for v in row
            ],
        )

    console.print(table)


def print_presence_matrix(variable_map: dict, reveal: bool = False):
    files, rows = build_matrix_data(variable_map)
    table = build_table(files, center_values=True)

    for key, row in rows:
        table.add_row(
            key,
            *["✅" if v is not None else "❌" for v in row],
        )

    console.print(table)


def build_table(files: list[str], center_values: bool = False) -> Table:
    table = Table(
        show_header=True,
        header_style="bold magenta",
        box=box.ROUNDED,
        border_style="bright_black",
    )
    table.add_column("VARIABLE", style="bold")

    for col in files:
        table.add_column(
            col,
            style="cyan",
            justify="center" if center_values else "default",
        )

    return table
