import os
import pathlib
import subprocess
import shutil

from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName
from swift_portal_downloader.portal.download.observation_id_to_wget_command import (
    observation_id_to_wget_command,
)
from swift_portal_downloader.swift.swift_downloadable_data_types import (
    SwiftDownloadableDataType,
)
from swift_portal_downloader.swift.swift_observation_id import SwiftObservationID


# TODO: document the server-side folder structure here, because we use it as our structure after download
"""
"""


def has_been_downloaded(
    base_dir: pathlib.Path,
    canonical_name: CanonicalCometName,
    observation_id: SwiftObservationID,
    data_type: SwiftDownloadableDataType,
) -> bool:
    """
    Checks for the existence of the folder associated with the given data type and observation id
    """
    data_folder_path = construct_full_data_folder_path(
        base_dir=base_dir,
        canonical_name=canonical_name,
        observation_id=observation_id,
        data_type=data_type,
    )
    return data_folder_path.exists()


def construct_download_destination_path(
    base_dir: pathlib.Path, canonical_name: CanonicalCometName
) -> pathlib.Path:
    """
    The directory we mave a completed download to: the data is moved under a folder with its canonical name for grouping by comet
    """
    return base_dir / pathlib.Path(canonical_name)


def construct_temporary_download_path(base_dir: pathlib.Path) -> pathlib.Path:
    """
    The directory where we download data before we move it into its proper place so we can avoid pollution from partial downloads
    in the main data directories
    """
    return base_dir / pathlib.Path("download_temp")


def construct_full_data_folder_path(
    base_dir: pathlib.Path,
    canonical_name: CanonicalCometName,
    observation_id: SwiftObservationID,
    data_type: SwiftDownloadableDataType,
) -> pathlib.Path:
    return (
        base_dir
        / pathlib.Path(canonical_name)
        / pathlib.Path(observation_id)
        / pathlib.Path(data_type)
    )


def download_uncompressed(
    base_dir: pathlib.Path,
    canonical_name: CanonicalCometName,
    observation_id: SwiftObservationID,
    data_type: SwiftDownloadableDataType,
) -> None:

    # save current working directory
    original_path = os.getcwd()

    # have we already done this?
    if has_been_downloaded(
        base_dir=base_dir,
        canonical_name=canonical_name,
        observation_id=observation_id,
        data_type=data_type,
    ):
        # print("This data seems to exist - skipping.")
        return

    # find out how to get the data we want
    wget_command = observation_id_to_wget_command(
        observation_id=observation_id, data_type=data_type, overwrite=False
    )

    # cd into temp download dir
    tmp_path = construct_temporary_download_path(base_dir=base_dir)
    tmp_path.mkdir(exist_ok=True, parents=True)
    tmp_observation_path = tmp_path / pathlib.Path(observation_id)
    tmp_data_path = tmp_observation_path / pathlib.Path(data_type)
    os.chdir(tmp_path)
    # print(f"Downloading into {tmp_path}...")

    # download
    presult = subprocess.run(wget_command.split())
    if presult.returncode != 0:
        print(
            f"Error code {presult.returncode} while downloading comet {canonical_name}, observation id {observation_id} for data type {data_type}"
        )
        return

    # restore working directory
    os.chdir(original_path)

    # make sure the directory to hold our downloaded data exists
    dest_data_path = construct_full_data_folder_path(
        base_dir=base_dir,
        canonical_name=canonical_name,
        observation_id=observation_id,
        data_type=data_type,
    )
    dest_data_path.mkdir(exist_ok=True, parents=True)

    # move the downloaded data to its place now that it is done
    os.rename(tmp_data_path, dest_data_path)

    # clean up the empty directories
    shutil.rmtree(tmp_observation_path)
