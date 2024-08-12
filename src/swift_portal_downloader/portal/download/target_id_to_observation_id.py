import requests

from swift_portal_downloader.swift.swift_observation_id import SwiftObservationID
from swift_portal_downloader.swift.swift_target_id import SwiftTargetID


# Function to generate a list of all obsids from a given tid
def swift_target_id_to_swift_observation_id(
    target_id: SwiftTargetID,
) -> list[SwiftObservationID]:
    """
    For any given target id, there may be multiple observations in their own directories,
    with the naming scheme {target id}001/, {target id}002/, etc.
    so we let the server give us the appropriate wget commands because it knows how
    many observations each target id has and what they are called

    We cannot assume that the observations start at 001 and are numbered sequentially! Sometimes numbers are skipped
    or are deleted, so we have to bug the server like this.
    """

    # Generate the wget command and run it
    # Timeout set to none to ensure https request does not drop (issue for mass search)
    base_wget_url = f"https://www.swift.ac.uk/archive/download.sh?reproc=1&tid={target_id}&source=obs&subdir=auxil"
    wget_response = requests.get(base_wget_url, timeout=None)

    # Get just a list of wget commands from the responses we got
    wget_commands = [line for line in wget_response.text.splitlines() if "wget" in line]
    urls = [command.split()[-1] for command in wget_commands]

    # Iterates through each wget url created
    swift_observation_ids = [url[39:-7] for url in urls]

    return swift_observation_ids
