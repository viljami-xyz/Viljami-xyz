""" Service to fetch data from Goodreads """

import pathlib
from typing import List, Union

import requests
from bs4 import BeautifulSoup

from app.services.models import BookCard

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


def fetch_books():
    """Fetch books from Goodreads
    # ? Note that this only returns latest 30 added books
    """
    my_books = []
    request = requests.get(URL, timeout=5)

    bs_fetch = BeautifulSoup(request.text, "html.parser")
    tbody = bs_fetch.find(id="booksBody")
    list_of_books = tbody.find_all("tr")
    for book in list_of_books:
        title = book.find("td", {"class": "field title"}).find("a").text
        author = book.find("td", {"class": "field author"}).find("a").text
        cover_image = book.find("td", {"class": "field cover"}).find("img").get("src")

        date_added = book.find("td", {"class": "field date_added"}).find("span").text

        read_state = (
            book.find("td", {"class": "field rating"}).find("span").get("title")
        )
        new_book = BookCard(
            title=parse_name(title),
            author=parse_name(author),
            cover_image=parse_name(cover_image),
            date_added=parse_name(date_added),
            read_state=get_state(read_state),
            rating=None,
            review=None,
        )
        my_books.append(new_book)
    return my_books


def nested_books(list_of_books) -> List[List[dict]]:
    """Load repositories from file"""
    list_of_books = [BookCard.from_orm(book) for book in list_of_books]
    return [list_of_books[i : i + 3] for i in range(0, len(list_of_books), 3)]
