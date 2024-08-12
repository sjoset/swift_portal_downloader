import pathlib

import questionary
from rich.console import Console
from rich.panel import Panel

from swift_portal_downloader.config.spd_config import (
    SwiftPortalDownloaderConfig,
    write_swift_portal_downloader_config,
)
from swift_portal_downloader.swift.swift_downloadable_data_types import (
    SwiftDownloadableDataType,
)


# TODO: add menu entry point for viewing/altering config, maybe ask for missing entries instead of erroring out
def create_config_tui() -> SwiftPortalDownloaderConfig | None:

    c = Console()
    c.print(Panel("Portal Downloader Configuration", expand=True), justify="center")
    c.print(
        "Welcome to the SWIFT portal downloader!  We need a [cyan]few[/] things before we get started."
    )

    data_download_path = get_config_download_path_tui()

    if data_download_path is None:
        return None

    data_types_to_download = get_config_data_types_tui()

    if data_types_to_download is None or len(data_types_to_download) == 0:
        return None

    spdc = SwiftPortalDownloaderConfig(
        download_path=data_download_path,
        data_type_list=[str(x) for x in data_types_to_download],  # type: ignore
    )
    print(f"{spdc=}")
    write_swift_portal_downloader_config(spdc=spdc)

    return spdc


def get_config_download_path_tui() -> pathlib.Path | None:

    # select directory to hold downloads
    data_download_path = questionary.path(
        "Directory to hold SWIFT data: ", qmark=""
    ).ask()

    return data_download_path


def get_config_data_types_tui() -> list | None:

    data_types_to_download = questionary.checkbox(
        "Select data types to download:",
        SwiftDownloadableDataType.all_data_types(),
        qmark="",
    ).ask()

    return data_types_to_download
