from typing import TypeAlias

from swift_portal_downloader.swift.swift_target_id import SwiftTargetID

SwiftObservationID: TypeAlias = str


def swift_target_id_from_observation_id(obsid: SwiftObservationID) -> SwiftTargetID:
    """
    Chop off the three right-most digits
    """
    # TODO: we can just do return obsid[:-3]
    orbit_int = round(int(obsid) / 1000)
    return SwiftTargetID(f"{orbit_int:08}")


def swift_observation_id_from_int(number: int) -> SwiftObservationID | None:
    """
    Observation IDs are 11-digit, left-0-padded strings that represent an integer
    """
    converted_string = f"{number:011}"
    if len(converted_string) != 11:
        return None
    return SwiftObservationID(converted_string)
