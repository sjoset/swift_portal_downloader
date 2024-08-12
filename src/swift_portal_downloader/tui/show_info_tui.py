import pathlib
from importlib.resources import files

from rich.console import Console
from rich.markdown import Markdown


def get_info_md_path() -> pathlib.Path:
    info_md_path: pathlib.Path = files("swift_portal_downloader.tui").joinpath("tui_info.md")  # type: ignore
    return info_md_path


def show_info_tui() -> None:

    c = Console()
    c.clear()
    info_md_path = get_info_md_path()

    with info_md_path.open() as f:
        markdown = Markdown(f.read())
        c.print(markdown)

    input()
