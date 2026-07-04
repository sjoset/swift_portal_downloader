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

    # check to see if it is in the manually renamed set
    manual_name = manual_canonical_name_lookup(
        # swift_target_name=swift_target_name, name_scheme_path=name_scheme_path
        swift_target_name=swift_target_name
    )

    if manual_name is not None:
        canonical_name = manual_name
    elif long_name is not None:
        canonical_name = long_name
    elif short_name is not None:
        canonical_name = short_name
    else:
        print(
            f"No canonical name found for {swift_target_name}! Update manual fix list!"
        )
        canonical_name = "fixme"

    # Replace all canonical_names / with _ for when we format our download_dir
    return canonical_name.replace("/", "_")
