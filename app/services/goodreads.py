""" Service to fetch data from Goodreads """

import json
import pathlib
import time
from typing import List, Union

from aiohttp import ClientSession
from bs4 import BeautifulSoup

URL = "https://www.goodreads.com/review/list/168386063-viljami-kilkkil?shelf=%23ALL%23"
LISTID = "booksBody"
saved_books = pathlib.Path("app/static/books.json")


def parse_name(text: str) -> str:
    """Remove whitespace and break lines from name"""
    return " ".join(text.replace("\n", "").strip().split())


def get_state(text: Union[str, None]) -> bool:
    """Find an integer from string"""
    if not text:
        return False
    return True


class GoodReadsBooks:
    """Fetch books from Goodreads"""

    timestamp = time.time()

    async def fetch_books(self):
        """Fetch books from Goodreads
        # ? Note that this only returns latest 30 added books
        """
        if not self.fetch_interval and saved_books.exists():
            return self.load_books_in_ball
        my_books = []
        async with ClientSession() as client:
            async with client.get(URL) as request:
                # request = requests.get(URL, timeout=5)

                bs_fetch = BeautifulSoup(await request.text(), "html.parser")
                tbody = bs_fetch.find(id="booksBody")
                list_of_books = tbody.find_all("tr")
                for book in list_of_books:
                    title = book.find("td", {"class": "field title"}).find("a").text
                    author = book.find("td", {"class": "field author"}).find("a").text
                    cover_image = (
                        book.find("td", {"class": "field cover"}).find("img").get("src")
                    )

                    date_added = (
                        book.find("td", {"class": "field date_added"}).find("span").text
                    )

                    read_state = (
                        book.find("td", {"class": "field rating"})
                        .find("span")
                        .get("title")
                    )
                    new_book = {
                        "title": parse_name(title),
                        "author": parse_name(author),
                        "cover": parse_name(cover_image),
                        "date_added": parse_name(date_added),
                        "read_state": get_state(read_state),
                    }
                    my_books.append(new_book)
        self.save_books(my_books)
        return self.load_books_in_ball

    @property
    def fetch_interval(self) -> bool:
        """Check the difference between timestamp and current time,
        if more than 1 hour, return True"""
        return time.time() - self.timestamp > 3600

    def save_books(self, list_of_books: List[dict]):
        """Save repositories to file"""
        with open(saved_books, "w", encoding="UTF-8") as file:
            json.dump(list_of_books, file)

    @property
    def load_books(self) -> List[dict]:
        """Load repositories from file"""
        with open(saved_books, "r", encoding="UTF-8") as file:
            list_of_books = json.load(file)
        return list_of_books

    @property
    def load_books_in_ball(self) -> List[List[dict]]:
        """Load repositories from file"""
        with open(saved_books, "r", encoding="UTF-8") as file:
            list_of_books = json.load(file)
        return [list_of_books[i : i + 3] for i in range(0, len(list_of_books), 3)]
