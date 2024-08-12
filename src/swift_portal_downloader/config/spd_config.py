import pathlib
import yaml
from dataclasses import dataclass, asdict

from swift_portal_downloader.swift.swift_downloadable_data_types import (
    SwiftDownloadableDataType,
)


@dataclass
class SwiftPortalDownloaderConfig:
    download_path: pathlib.Path
    data_type_list: list[SwiftDownloadableDataType]


def get_swift_portal_downloader_config_path() -> pathlib.Path:
    return pathlib.Path("spd_config.yaml")


def write_swift_portal_downloader_config(spdc: SwiftPortalDownloaderConfig) -> None:

    spdc_dict = asdict(spdc)
    config_path = get_swift_portal_downloader_config_path()
    # config_path.touch()

    with open(config_path, "w") as spdc_config_file:
        yaml.dump(spdc_dict, spdc_config_file)


def read_swift_portal_downloader_config() -> SwiftPortalDownloaderConfig | None:
    # TODO: add some validation here

    if not get_swift_portal_downloader_config_path().exists():
        return None

    with get_swift_portal_downloader_config_path().open() as spdc_config_file:
        spdc_dict = yaml.safe_load(spdc_config_file)

    return SwiftPortalDownloaderConfig(**spdc_dict)
