import pathlib

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.progress import track

from swift_portal_downloader.comet_db.comet_db import CometDatabaseEntry
from swift_portal_downloader.portal.download.target_id_to_observation_id import (
    swift_target_id_to_swift_observation_id,
)
from swift_portal_downloader.portal.download.uncompressed_download import (
    download_uncompressed,
    has_been_downloaded,
)
from swift_portal_downloader.swift.swift_downloadable_data_types import (
    SwiftDownloadableDataType,
)


def download_comet_database_entry(
    base_dir: pathlib.Path,
    db_entry: CometDatabaseEntry,
    data_type: SwiftDownloadableDataType,
) -> None:

    c = Console()

    # find all of the observation ids associated with this target id
    observation_ids = swift_target_id_to_swift_observation_id(
        target_id=db_entry.target_id
    )

    # have we already done this?
    if all(
        [
            has_been_downloaded(
                base_dir=base_dir,
                canonical_name=db_entry.canonical_name,
                observation_id=obsid,
                data_type=data_type,
            )
            for obsid in observation_ids
        ]
    ):
        # c.print(f"[red]Skipping target id {db_entry.target_id}!")
        return

    # show the observation ids we found associated with this target id
    c.print(
        f"Expanding target id [cyan]{db_entry.target_id:08d}[/] into observation ids:",
    )
    panels = [Panel(f"[light_sky_blue1]{x}", expand=True) for x in observation_ids]
    columns = Columns(panels, equal=True)
    c.print(columns, justify="center")

    # did the server report more observations than it did when we made the database?
    if db_entry.number_of_observations != len(observation_ids):
        c.print("Warning:")
        c.print(
            f"The comet database says there are {db_entry.number_of_observations} for target ID {db_entry.target_id},"
        )
        c.print(
            f"but the website says there are {len(observation_ids)} - maybe the comet db is out of date?"
        )
        c.print("[red]Not downloading![/]")
        input()
        return

    for observation_id in track(
        observation_ids,
        description=f"Downloading [light_sky_blue1]{data_type}[/] data ...",
    ):
        download_uncompressed(
            base_dir=base_dir,
            canonical_name=db_entry.canonical_name,
            observation_id=observation_id,
            data_type=data_type,
        )
