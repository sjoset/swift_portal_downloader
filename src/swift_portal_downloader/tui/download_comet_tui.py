import pandas as pd
import questionary
from rich.columns import Columns
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.text import Text
from rich import print

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


# TODO: duplicated in search_comet_db_tui
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


# TODO: duplicated in search_comet_db_tui
def dataframe_to_rich_table(df: pd.DataFrame) -> Table:

    t = Table(style="magenta", title=f"[light_sky_blue1]Available for download")
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
    print(make_db_info_panel(comet_db_df=comet_db_df))

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
    comet_t = dataframe_to_rich_table(comet_df)
    # comet_t_centered = Align.center(comet_t)
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

    c.print("Will download data types:")
    for data_type in spdc.data_type_list:
        c.print(
            f"[light_sky_blue1]{data_type}[/]: {total_available_observations - num_observations_downloaded[data_type]}"
        )

    do_download = questionary.confirm("Download data?", qmark="").ask()

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
