from swift_portal_downloader.portal.download.wget_command import WgetCommand
from swift_portal_downloader.swift.swift_downloadable_data_types import (
    SwiftDownloadableDataType,
)
from swift_portal_downloader.swift.swift_observation_id import SwiftObservationID


def observation_id_to_wget_command(
    observation_id: SwiftObservationID,
    data_type: SwiftDownloadableDataType,
    overwrite: bool,
) -> WgetCommand:
    """
    --cut-dirs=2 is necessary to cut the archive/reproc folders off of the server-side directory structure so we can download to
    a directory named {observation_id}
    """

    if overwrite is False:
        overwrite_option = "-nc "
    else:
        overwrite_option = ""
    wget_command = (
        "wget "
        + overwrite_option
        + f"-q -w 2 -nH --cut-dirs=2 -r --no-parent --reject index.html*,robots.txt*  -erobots=off http://www.swift.ac.uk/archive/reproc/{observation_id}/{data_type}/"
    )
    return wget_command
