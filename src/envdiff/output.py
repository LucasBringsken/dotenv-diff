from pandas import DataFrame
from rich.console import Console, Group
from rich.panel import Panel
from rich.rule import Rule
from rich.table import Table
from rich import box

console = Console()


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
