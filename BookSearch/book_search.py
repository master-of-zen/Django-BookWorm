"""
Processing request, returning books info
"""
# Standard libraries
import logging
import string
from io import BytesIO
from urllib import request
from urllib.parse import urlencode

# Imported modules
from requests import get
from bs4 import BeautifulSoup

# Own modules
from BookSearch.async_stuff import scrap_web_pages

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def get_request(book_request) -> dict:
    # Process user request and return dictionary with info to search with

    # Search attributes
    lang = ['en', 'ru', 'fr', 'de']
    ext = ['pdf', 'epub', 'fb2', 'djvu', 'doc']
    book = {}
    params = []
    request_text = []

    # Separate parameters and book title
    for i in book_request.split():
        if i.startswith('.') and len(i) > 1:
            param = i.lower()
            params.append(param[1:])
        else:
            request_text.append(i)
    book['title'] = ' '.join(request_text)

    for i in params:
        if i in lang:
            book['lang'] = i
        elif i in ext:
            book['ext'] = i
        elif i.isdigit():
            book['year'] = int(i)

    logging.info(f'Parsed book: {book}')
    return book


def get_attributes(book_attribute) -> dict:
    # Book info dictionary
    book = {}

    # Removing numbers from back, not pretty stuff but works
    isdigit = True
    title = book_attribute[2].text
    while isdigit and len(title.split()) > 1:
        if title.split()[-1].translate(str.maketrans('', '', string.punctuation)).isdigit():
            title = title.split()[:-1]
            title = ' '.join(title)
        else:
            isdigit = False

    # Setting attributes
    book['title'] = title  # Title
    book['author'] = book_attribute[1].text
    book['language'] = book_attribute[6].text[:2]
    book['size'] = book_attribute[7].text
    book['ext'] = book_attribute[8].text
    book['link'] = book_attribute[9].a.attrs['href']

    # Try get year, because sometimes it have weird formating like 04-1984, 1984.4 etc
    try:
        book['year'] = int(book_attribute[4].text)
    except ValueError:
        pass

    return book


def sort_books(all_books, book) -> list:
    # Removing all books that not match parameters

    # Check for language
    if book.get('lang'):
        for i in list(all_books):
            if i.get('lang'):
                if i.get('lang').lower() != book.get('lang').lower():
                    all_books.remove(i)

    # Check for book extension
    if book.get('ext'):
        for i in list(all_books):
            if i.get('ext').lower() != book.get('ext').lower():
                all_books.remove(i)

    # Check for year
    if book.get('year'):
        for i in list(all_books):
            if i.get('year') != book.get('year'):
                all_books.remove(i)

    logging.info(f'Found valid books {len(all_books)}')
    return all_books


def search(book_request) -> list:
    book = get_request(book_request)
    # Given tuple with book info, search for book on libgen and return all books that relevant
    try:
        # Scrap libgen search page for books data
        logger.info(f'Searching for book: {book.get("title")}')
        sort = {}
        all_books = []
        if book.get('year'):
            sort = {'sort': 'year', 'sortmode': 'DESC'}

        # Compose urls
        urls = [f'http://libgen.is/search.php?&{urlencode({"req": book.get("title"), "res": 100,  **sort, "page":page,})}'
                for page in range(1, 11)]

        # Extract all books from page html
        for html in scrap_web_pages(urls):
            soup = BeautifulSoup(html, 'lxml')
            books = soup.find_all('tr')[3:-1]  # Get all books with their info
            for raw_book in books:
                book_attribute = raw_book.find_all('td')
                if len(book_attribute) >= 10:
                    all_books.append(get_attributes(book_attribute))

        logging.info(f'Found books: {len(all_books)}')

        # Filter books if required
        if book.get('ext') or book.get('lang') or book.get('year'):
            all_books = sort_books(all_books, book)
        return all_books

    except Exception as E:
        logging.error(f'Error {E} in search')
        return []






