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
from text import print_centered_text
from licences import select_license


class Core(object):

    """Docstring for Core. """

    def __init__(
        self,
        author: str,
        year: int,
        title: str,
        description: str,
        license_: list,
        path: str,
    ):
        """
        :author: Author Name
        :year: Year of creation
        :title: Program Title
        :description: Program description
        :license_: License type
        :path: Program running path

        """

        self._author = author
        self._year = year
        self._title = title
        self._description = description
        self._path = path
        self._license = select_license(license_, author, title, description, year)

    def start_ui(self):
        """
        :returns: Main screen

        """
        page = Main(self._license)
        page.run()


class Main(Core):

    """Main Screen"""

    def __init__(self, license_):
        """TODO: to be defined. """
        super(Core, self).__init__()
        self._license = license_
        self._options = {
            0: "Quit",
            1: "New Search",
            2: "Browse Database",
        }

    def run(self):
        @head
        def print_license():
            print_centered_text(self._license)

        @body
        def print_options():
            print(
                *[
                    f"[{n}] {self._options[n]} "
                    for n, title in enumerate(self._options)
                ],
            )

        @footer
        def selector():
            resp = numeric_selector(self._options)
            if resp == 0:
                sys.exit()
            if resp == 1:
                Search().run()
            if resp == 2:
                pass

        os.system("clear")
        print_license()
        print_options()
        selector()


class Search(Core):

    """Docstring for Search. """

    def __init__(self):
        """TODO: to be defined. """
        super(Core, self).__init__()

    def run(self):
        os.system("clear")
        print("Search Page")


if __name__ == "__main__":
    path = os.getcwd()
    ui = Core("Kajetan", 2020, "MoMA", "Moma museum artwork web scraper", "GPL3", path)
    ui.start_ui()
