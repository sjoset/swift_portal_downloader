import pandas as pd
from rich.console import Console

from swift_portal_downloader.comet_db.comet_db import (
    comet_database_entries_to_dataframe,
    read_comet_database,
)
from swift_portal_downloader.comet_db.download_comet_db import download_comet_db
from swift_portal_downloader.tui.rich_display import dataframe_to_rich_table


def download_comet_db_tui() -> None:

    old_comet_db = read_comet_database()
    old_comet_df = comet_database_entries_to_dataframe(comet_db_entries=old_comet_db)

    print("Downloading list of all known comet observations ...")
    download_comet_db()

    updated_comet_db = read_comet_database()
    updated_comet_df = comet_database_entries_to_dataframe(
        comet_db_entries=updated_comet_db
    )

    new_observations = pd.concat([old_comet_df, updated_comet_df]).drop_duplicates(
        keep=False
    )

    c = Console()
    if len(new_observations) == 0:
        c.print("[cyan]No new observations!", justify="center")
    else:
        c.print(
            dataframe_to_rich_table(
                df=new_observations, table_title="[light_sky_blue1]New observations"
            ),
            justify="center",
        )
    input()
