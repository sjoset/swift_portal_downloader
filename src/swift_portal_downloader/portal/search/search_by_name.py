import requests

from bs4 import BeautifulSoup


from swift_portal_downloader.comet_db.comet_db import CometDatabaseEntry
from swift_portal_downloader.naming.name_conversion import (
    swift_target_name_to_canonical_name,
)


def generate_search_portal_url(search_term: str) -> str:
    """
    Takes a search term and produces a url string for searching the swift dead portal by target name (search_term)
    """

    # Construct the search url
    base_search_url = "https://www.swift.ac.uk/dead_portal/getobject.php"
    search_url = base_search_url + "?name=" + search_term + "&submit=Search+Names"

    return search_url


def soup_to_comet_db_entries(search_soup: BeautifulSoup) -> list[CometDatabaseEntry]:
    """
    search_soup is the resulting BeautifulSoup object constructed from the web page by searching the swift portal by target name
    If the structure of the website changes, this function will need revision
    """

    # Get the main results table
    results_table = search_soup.find("table", {"class": "chTable"})

    if results_table is None:
        return []

    # Ignore the first row with the names of the columns, and the last row with links for all of the data
    table_rows = results_table.find_all("tr")[1:-1]  # type: ignore

    # .contents is a list, our table has only one element in it, so take contents[0]
    swift_target_ids = [
        row.find("td", {"headers": "row_targ"}).contents[0] for row in table_rows
    ]
    swift_target_names = [
        row.find("td", {"headers": "row_name"}).contents[0] for row in table_rows
    ]
    num_observations = [
        row.find("td", {"headers": "row_num"}).contents[0] for row in table_rows
    ]

    cdb_entries = [
        CometDatabaseEntry(
            swift_target_name=swift_target_name,
            number_of_observations=int(number_of_observations),
            target_id=target_id,
            canonical_name=swift_target_name_to_canonical_name(
                swift_target_name=swift_target_name
            ),
        )
        for swift_target_name, number_of_observations, target_id in zip(
            swift_target_names, num_observations, swift_target_ids
        )
    ]

    return cdb_entries


def search_portal_by_target_name(search_term: str) -> list[CometDatabaseEntry]:

    search_url = generate_search_portal_url(search_term=search_term)

    # Download the search page and parse it
    page_html = requests.get(search_url)
    search_soup = BeautifulSoup(page_html.text, features="lxml")

    return soup_to_comet_db_entries(search_soup=search_soup)
