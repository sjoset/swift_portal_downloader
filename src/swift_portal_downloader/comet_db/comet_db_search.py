import pandas as pd

from swift_portal_downloader.comet_db.comet_db import (
    CometDatabaseEntry,
    comet_database_entries_to_dataframe,
    dataframe_to_comet_database_entries,
)


def search_comet_db_by_canonical_name(
    comet_db_entries: list[CometDatabaseEntry], search_term: str
) -> list[CometDatabaseEntry]:

    df = comet_database_entries_to_dataframe(comet_db_entries=comet_db_entries)

    results_df: pd.DataFrame = df[df.canonical_name.contains(search_term)]  # type: ignore

    return dataframe_to_comet_database_entries(df=results_df)
