from swift_portal_downloader.comet_db.comet_db import write_comet_database
from swift_portal_downloader.portal.search.all_comet_search import (
    search_portal_for_all_comets,
)


def download_comet_db() -> None:

    comet_db_entries = search_portal_for_all_comets()
    write_comet_database(comet_db_entries=comet_db_entries)
