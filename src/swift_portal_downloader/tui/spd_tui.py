import sys

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.align import Align

from swift_portal_downloader.comet_db.comet_db import get_comet_db_path
from swift_portal_downloader.config.spd_config import (
    read_swift_portal_downloader_config,
)
from swift_portal_downloader.tui.create_config_tui import create_config_tui
from swift_portal_downloader.tui.download_comet_db_tui import download_comet_db_tui
from swift_portal_downloader.tui.download_comet_tui import download_comet_tui
from swift_portal_downloader.tui.search_comet_db_tui import search_comet_db_tui
from swift_portal_downloader.tui.show_info_tui import show_info_tui


def construct_main_menu() -> list:

    menu_choices = []
    if not get_comet_db_path().exists():
        menu_choices.append("Download comet database")
    else:
        menu_choices.extend(
            ["Update comet database", "Comet database info", "Download comet data"]
        )

    menu_choices.extend(["Information", "Exit"])

    return menu_choices


def main():

    c = Console()
    spdc = read_swift_portal_downloader_config()
    if spdc is None:
        spdc = create_config_tui()
        if spdc is None:
            print("No valid config! Exiting.")
            exit(1)

    banner_panel = Panel("Swift Portal Downloader")
    banner = Align.center(banner_panel)

    while True:
        c.clear()
        c.print(banner)
        main_menu_choices = construct_main_menu()
        main_menu_choice = questionary.select(
            "",
            choices=main_menu_choices,
            use_shortcuts=True,
            qmark="",
            instruction=" ",
        ).ask()

        match main_menu_choice:
            case "Download comet database":
                download_comet_db_tui()
            case "Update comet database":
                download_comet_db_tui()
            case "Comet database info":
                search_comet_db_tui()
            case "Download comet data":
                download_comet_tui(spdc=spdc)
            case "Information":
                show_info_tui()
            case "Exit":
                break


if __name__ == "__main__":
    sys.exit(main())
