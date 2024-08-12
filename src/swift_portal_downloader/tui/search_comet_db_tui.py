import pandas as pd
import questionary
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import print

from swift_portal_downloader.comet_db.comet_db import (
    CometDatabaseEntry,
    comet_database_entries_to_dataframe,
    read_comet_database,
)
from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName


def make_db_info_panel(comet_db_df: pd.DataFrame):

    num_comets = comet_db_df.canonical_name.nunique()
    num_observations = comet_db_df.number_of_observations.sum()
    num_targets = comet_db_df.target_id.nunique()

    ptext = Text()
    ptext.append("SWIFT Comet Database Summary", style="bold cyan")
    ptext = Align.center(ptext)
    p = Panel(ptext, highlight=True, expand=True, style="magenta")

    t = Table(style="magenta")
    t.add_column("[cyan]Number of comets")
    t.add_column("[cyan]Number of target IDs")
    t.add_column("[cyan]Total observations")
    table_entry_color = "[medium_orchid3]"
    t.add_row(
        f"{table_entry_color}{num_comets}",
        f"{table_entry_color}{num_targets}",
        f"{table_entry_color}{num_observations}",
    )

    centered_table = Align.center(t)

    return Group(p, centered_table)


def dataframe_to_rich_table(df: pd.DataFrame) -> Table:

    t = Table(style="magenta")
    for col in df.columns:
        t.add_column(f"[cyan]{col}")

    table_entry_color = "[light_sky_blue1]"
    for _, row in df.iterrows():
        t.add_row(
            f"{table_entry_color}{row.swift_target_name}",
            f"{table_entry_color}{row.number_of_observations}",
            f"{table_entry_color}{row.target_id:08d}",
            f"{table_entry_color}{row.canonical_name}",
        )

    return t


def search_comet_db_tui() -> None:

    q_custom_style = questionary.Style(
        [
            ("question", "fg:#dbafad"),
            ("selected", "fg:#e7e7ea"),
            ("answer", "fg:#c74a77 bold"),
            ("disabled", "fg:#82787f italic"),
        ]
    )

    c = Console()
    c.clear()

    comet_db_entries = read_comet_database()
    comet_db_df = comet_database_entries_to_dataframe(comet_db_entries=comet_db_entries)

    print(make_db_info_panel(comet_db_df=comet_db_df))

    available_comets = list(set(comet_db_df.canonical_name))
    selected_comet = questionary.autocomplete(
        "Select comet to query: (control-c to cancel)",
        choices=available_comets,
        style=q_custom_style,
        qmark="",
    ).ask()

    if selected_comet is None:
        return

    c.print(f"Results for [cyan]{selected_comet}:", justify="left")
    comet_df = comet_db_df[comet_db_df.canonical_name == selected_comet].copy()
    t = Align.center(dataframe_to_rich_table(comet_df))  # type: ignore
    c.print(t)
    c.print(
        f"Total observations: {comet_df.number_of_observations.sum()}", justify="center"
    )
    input()
