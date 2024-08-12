import re
from typing import TypeAlias

from swift_portal_downloader.swift.swift_target_name import SwiftTargetName


CanonicalCometName: TypeAlias = str


# Function to match comet_name that may contain C/ or Comet#### formatting
def match_long_period_name(
    swift_target_name: SwiftTargetName,
) -> CanonicalCometName | None:
    """
    Searches swift_target_name string for anything resembling a long-period comet naming convention, returning None if not successful.
    """

    # Match naming convention of long period comets: C/[YEAR][one optional space character][one to two letters][one to two digits]
    long_period_match = re.search(
        "C/[0-9]{4}\\s?[A-Z]{1,2}[0-9]{1,2}", swift_target_name
    )
    if long_period_match:
        # Get the matched part of the string if there was a match
        long_period_name = long_period_match.group() if long_period_match else None
    else:
        # Try the same match but instead of "C/...", look for "Comet..."
        long_period_match = re.search(
            "Comet[0-9]{4}\\s?[A-Z]{1,2}[0-9]{1,2}", swift_target_name
        )
        if long_period_match:
            long_period_name = re.sub("Comet", "C/", long_period_match.group())
        else:
            long_period_name = None

    return long_period_name


# Function to match comet_name that may contain P/ or ##P formatting
def match_short_period_name(
    swift_target_name: SwiftTargetName,
) -> CanonicalCometName | None:
    """
    Searches swift_target_name string for anything resembling a short-period comet naming convention, returning None if not successful.
    """

    # Try to find P/[YEAR][one to two characters][one to three numbers]
    short_period_match = re.search("P/[0-9]{4}[A-Z]{1,2}[0-9]{1,3}", swift_target_name)
    if short_period_match:
        short_period_name = short_period_match.group() if short_period_match else None
    else:
        # Match naming convention of short period comets: [1 to 3 digits]P
        short_period_match = re.search("[0-9]{1,3}P", swift_target_name)
        if short_period_match:
            short_period_name = short_period_match.group()
        else:
            short_period_name = None

    return short_period_name
