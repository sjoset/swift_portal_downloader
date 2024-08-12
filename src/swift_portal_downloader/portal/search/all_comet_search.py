import itertools

from rich.console import Console
from rich.progress import track

from swift_portal_downloader.comet_db.comet_db import CometDatabaseEntry
from swift_portal_downloader.portal.search.search_by_name import (
    search_portal_by_target_name,
)


def search_portal_for_all_comets() -> list[CometDatabaseEntry]:
    """
    Search the portal for any swift target names that might be comets and return the list of results
    """

    all_comet_search_terms = ["Comet", "P/", "C/"]

    # console = Console()
    # Console()
    # print()

    # Collect all search results from search_terms
    results_list = []
    for search_term in track(
        all_comet_search_terms, description="[cyan]Searching portal ...[/]"
    ):
        results_list.append(search_portal_by_target_name(search_term=search_term))

    # we have a list of lists - flatten them into one large list
    return list(itertools.chain(*results_list))
