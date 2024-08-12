import yaml
from typing import TypeAlias
from importlib.resources import files

from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName
from swift_portal_downloader.swift.swift_target_name import SwiftTargetName


ManualRenamingScheme: TypeAlias = dict[SwiftTargetName, CanonicalCometName]


def get_internal_renaming_scheme() -> ManualRenamingScheme:

    internal_renaming_file_path = files("swift_portal_downloader.naming").joinpath(
        "swift_target_name_to_canonical_name.yaml"
    )

    with internal_renaming_file_path.open() as file:
        internal_renaming_scheme = yaml.safe_load(file)

    return internal_renaming_scheme
