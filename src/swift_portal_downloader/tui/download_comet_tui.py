import pathlib

import pandas as pd
import questionary
from rich.columns import Columns
from rich.console import Console
from rich.table import Table
from rich.align import Align

from swift_portal_downloader.comet_db.comet_db import (
    comet_database_entries_to_dataframe,
    dataframe_to_comet_database_entries,
    read_comet_database,
)
from swift_portal_downloader.config.spd_config import SwiftPortalDownloaderConfig
from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName
from swift_portal_downloader.portal.download.download_comet_db_entry import (
    download_comet_database_entry,
)
from swift_portal_downloader.portal.download.uncompressed_download import (
    construct_download_destination_path,
)
from swift_portal_downloader.swift.swift_downloadable_data_types import (
    SwiftDownloadableDataType,
)
from swift_portal_downloader.tui.rich_display import (
    dataframe_to_rich_table,
    make_comet_db_info_text,
)


def count_downloaded_observations(
    spdc: SwiftPortalDownloaderConfig,
    canonical_name: CanonicalCometName,
    data_type: SwiftDownloadableDataType,
) -> int:

    data_path = construct_download_destination_path(
        base_dir=spdc.download_path, canonical_name=canonical_name
    )
    subdirs_in_data_path = [x for x in data_path.glob("*") if x.is_dir()]
    data_type_observations = []
    for observation_dir in subdirs_in_data_path:
        data_type_observations.extend(
            [x for x in observation_dir.glob("*") if x.is_dir() and x.name == data_type]
        )

    return len(data_type_observations)


def download_comet_tui(spdc: SwiftPortalDownloaderConfig) -> None:

    # TODO: move to function
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

    # read in our comet db and show info
    comet_db_entries = read_comet_database()
    comet_db_df = comet_database_entries_to_dataframe(comet_db_entries=comet_db_entries)
    c.print(make_comet_db_info_text(comet_db_df=comet_db_df))

    available_comets = list(set(comet_db_df.canonical_name))
    selected_comet = questionary.autocomplete(
        "Select comet to download: (control-c to cancel)",
        choices=available_comets,
        style=q_custom_style,
        qmark="",
    ).ask()

    if selected_comet is None:
        return

    c.print(f"Results for [cyan]{selected_comet}:", justify="left")
    comet_df: pd.DataFrame = comet_db_df[comet_db_df.canonical_name == selected_comet].copy()  # type: ignore
    comet_t = dataframe_to_rich_table(
        comet_df, table_title=f"[light_sky_blue1]Available for download"
    )
    total_available_observations = comet_df.number_of_observations.sum()

    download_t = Table(
        style="magenta", title=f"[light_sky_blue1]Downloaded observations by type"
    )
    for data_type in SwiftDownloadableDataType.all_data_types():
        download_t.add_column(f"[cyan]{data_type}")

    num_observations_downloaded = {}
    num_observations_downloaded_text = {}
    for data_type in SwiftDownloadableDataType.all_data_types():
        data_type_count = count_downloaded_observations(
            spdc=spdc, canonical_name=selected_comet, data_type=data_type
        )
        num_observations_downloaded[data_type] = data_type_count
        num_observations_downloaded_text[data_type] = (
            f"[light_sky_blue1]{data_type_count}"
        )
    download_t.add_row(*num_observations_downloaded_text.values())

    c.print(Align.center(Columns([comet_t, download_t])))
    c.print(
        f"Total available observations on server: {total_available_observations}",
        justify="center",
    )
    c.print()

    c.print(
        f"Using download directory {spdc.download_path / pathlib.Path(selected_comet)}"
    )
    c.print("Will download data types:")
    for data_type in spdc.data_type_list:
        c.print(
            f"[light_sky_blue1]{data_type}[/]: {total_available_observations - num_observations_downloaded[data_type]}"
        )

    do_download = questionary.confirm(f"Download data?", qmark="").ask()

    if not do_download:
        return

    db_entries_to_download = dataframe_to_comet_database_entries(df=comet_df)

    c.clear()

    # loop over the database entries, which will contain unique target ids
    for entry in db_entries_to_download:
        for data_type in spdc.data_type_list:
            if num_observations_downloaded[data_type] == total_available_observations:
                c.print(
                    f"All data of type [light_sky_blue1]{data_type}[/] has been downloaded for [light_sky_blue1]{entry.target_id}[/] - skipping ..."
                )
                continue
            download_comet_database_entry(
                base_dir=spdc.download_path, db_entry=entry, data_type=data_type
            )

    c.print("[magenta]Done downloading!", justify="center")
    input()
