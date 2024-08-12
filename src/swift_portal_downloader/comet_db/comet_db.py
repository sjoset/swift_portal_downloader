import pathlib
from dataclasses import dataclass, asdict

import pandas as pd

from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName
from swift_portal_downloader.swift.swift_target_id import SwiftTargetID
from swift_portal_downloader.swift.swift_target_name import SwiftTargetName


# We want to search the portal for broad terms that should cover all comets and save the results in a csv as a local cache
@dataclass
class CometDatabaseEntry:
    swift_target_name: SwiftTargetName
    number_of_observations: int
    target_id: SwiftTargetID
    canonical_name: CanonicalCometName


def get_comet_db_path() -> pathlib.Path:
    return pathlib.Path("all_swift_comets.csv")


def comet_database_entries_to_dataframe(
    comet_db_entries: list[CometDatabaseEntry],
) -> pd.DataFrame:
    db_dict = [asdict(comet_db_entry) for comet_db_entry in comet_db_entries]
    df = pd.DataFrame(data=db_dict)
    return df


def dataframe_to_comet_database_entries(df: pd.DataFrame) -> list[CometDatabaseEntry]:
    return df.apply(lambda row: CometDatabaseEntry(**row), axis=1).to_list()


# def construct_comet_db_path(download_path: pathlib.Path) -> pathlib.Path:
#     return download_path / pathlib.Path("all_comets.csv")


def write_comet_database(
    # comet_db_entries: list[CometDatabaseEntry], download_path: pathlib.Path
    comet_db_entries: list[CometDatabaseEntry],
) -> None:
    """
    Takes the list given and writes it to a csv file
    download_path is taken from the config file, so that the comet db is stored one folder up from any data
    """

    # output_path = construct_comet_db_path(download_path=download_path)

    df = comet_database_entries_to_dataframe(comet_db_entries=comet_db_entries)
    df.to_csv(get_comet_db_path(), index=False)


# def read_comet_database(download_path: pathlib.Path) -> list[CometDatabaseEntry]:
def read_comet_database() -> list[CometDatabaseEntry]:
    """
    Returns the contents of the comet database
    download_path is taken from the config file, so that the comet db is stored one folder up from any data
    """

    # input_path = construct_comet_db_path(download_path=download_path)

    # df = pd.read_csv(input_path)
    df = pd.read_csv(get_comet_db_path())

    return dataframe_to_comet_database_entries(df=df)
