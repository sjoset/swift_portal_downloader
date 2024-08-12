import pandas as pd
from rich.console import Group
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text


def make_comet_db_info_text(comet_db_df: pd.DataFrame) -> Group:
    """
    Takes a dataframe built from list[CometDatabaseEntry] and returns a printable summary of the contents
    of the database overall
    """

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


def dataframe_to_rich_table(df: pd.DataFrame, table_title: str = "") -> Table:
    """
    Takes a dataframe built from list[CometDatabaseEntry] and returns a printable table of the entries
    """

    # t = Table(style="magenta", title=f"[light_sky_blue1]Available for download")
    t = Table(style="magenta", title=table_title)
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
