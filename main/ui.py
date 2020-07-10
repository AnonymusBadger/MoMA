import os
import sys
from checkers import (
    folder_exists_check,
    is_in_path,
    url_check,
    yes_no_sensitive,
    numeric_selector,
)
from fixers import set_first_page
from scraper import main as scraper
from decorators import head, body, footer
from text import center_text
from licences import select_license


class Head:
    @head
    def print(self):
        print(self._text)


class Options:
    @body
    def print(self):
        print(
            *[
                f"[{n}] {self._options[n][0]} "
                for n, title in enumerate(self._options, 1)
            ],
            "[0] Back",
        )


class Select:
    def print(self):
        return numeric_selector(self._options)


class Scrape:
    def __init__(self, path, *args, **kwargs):
        self._path = path

    @head
    def print(self):
        print("Hello! I'm scraper!")


class Database:
    pass


class MainMenu(Head, Options, Select):
    def __init__(self, licence_, author, title, description, year, *args, **kwargs):
        self._text = center_text(
            select_license(licence_, author, title, description, year,)
        )
        self._options = {
            1: ("New Search", Scrape),
            2: ("Brawse Data", Database),
        }

    def print(self):
        os.system("clear")
        Head.print(self)
        Options.print(self)
        resp = Select.print(self)
        if resp == 0:
            sys.exit()
        return self._options[resp][1]


class Ui(MainMenu, Scrape):
    def __init__(self, *args, **kwargs):
        MainMenu.__init__(self, *args, **kwargs)
        Scrape.__init__(self, *args, **kwargs)

    def start(self):
        next_manu = MainMenu.print(self)
        os.system("clear")
        next_manu.print(self)


if __name__ == "__main__":
    ui = Ui(
        author="Kajetan",
        year=2020,
        title="MoMA",
        description="Moma museum artwork web scraper",
        licence_="GPL3",
        path=None,
    )
    ui.start()
