import pandas as pd
import questionary
from rich.console import Console
from rich.align import Align

from swift_portal_downloader.comet_db.comet_db import (
    comet_database_entries_to_dataframe,
    read_comet_database,
)
from swift_portal_downloader.tui.rich_display import (
    dataframe_to_rich_table,
    make_comet_db_info_text,
)


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

    c.print(make_comet_db_info_text(comet_db_df=comet_db_df))

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
    comet_df: pd.DataFrame = comet_db_df[comet_db_df.canonical_name == selected_comet].copy()  # type: ignore
    t = Align.center(
        dataframe_to_rich_table(
            comet_df, table_title=f"[light_sky_blue1]Available for download"
        )
    )
    c.print(t)
    c.print(
        f"Total observations: {comet_df.number_of_observations.sum()}", justify="center"
    )
    input()
