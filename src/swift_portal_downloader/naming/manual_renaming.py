from swift_portal_downloader.naming.canonical_comet_name import CanonicalCometName
from swift_portal_downloader.naming.manual_renaming_scheme import (
    get_internal_renaming_scheme,
)
from swift_portal_downloader.swift.swift_target_name import SwiftTargetName


# When extracting the canonical comet name fails, we may have to fall back to looking up the canonical names of a few known cases
# of odd swift_target_names
# These mappings from swift_target_name -> CanonicalCometName were produced manually when initially examining the SWIFT data set
# and are stored internally in ./swift_target_name_to_canonical_name.yaml
def manual_canonical_name_lookup(
    swift_target_name: SwiftTargetName,
) -> CanonicalCometName | None:

    # TODO: this should only check the internal and external renaming schemes, and return None if not found - ask for user input elsewhere
    internal_renaming_scheme = get_internal_renaming_scheme()

    if swift_target_name in internal_renaming_scheme:
        canonical_name = internal_renaming_scheme[f"{swift_target_name}"]
    else:
        canonical_name = None

    return canonical_name
