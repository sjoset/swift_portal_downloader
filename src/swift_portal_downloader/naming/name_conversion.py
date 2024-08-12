from swift_portal_downloader.naming.canonical_comet_name import (
    CanonicalCometName,
    match_long_period_name,
    match_short_period_name,
)
from swift_portal_downloader.naming.manual_renaming import manual_canonical_name_lookup
from swift_portal_downloader.swift.swift_target_name import SwiftTargetName


def swift_target_name_to_canonical_name(
    # swift_target_name: SwiftTargetName, name_scheme_path: pathlib.Path | None = None
    swift_target_name: SwiftTargetName,
) -> CanonicalCometName:

    long_name = match_long_period_name(swift_target_name=swift_target_name)
    short_name = match_short_period_name(swift_target_name=swift_target_name)

    # TODO: maybe check to make sure we don't find a long and short period name for the same swift_target_name
    if long_name != None:
        canonical_name = long_name
    elif short_name != None:
        canonical_name = short_name
    else:
        canonical_name = manual_canonical_name_lookup(
            # swift_target_name=swift_target_name, name_scheme_path=name_scheme_path
            swift_target_name=swift_target_name
        )

    # Replace all canonical_names / with _ for when we format our download_dir
    return canonical_name.replace("/", "_")
