from typing import TypeAlias


SwiftTargetID: TypeAlias = str


def swift_target_id_from_int(number: int) -> SwiftTargetID | None:
    """
    Target IDs are 8-digit, left-0-padded strings that represent an integer
    """
    converted_string = f"{number:08}"
    if len(converted_string) != 8:
        return None
    return SwiftTargetID(converted_string)
