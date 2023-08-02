import requests
import urllib3
import os
import sys
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
import script
import json
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_book_page(url):
    response = requests.get(url, verify=False, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

def parse_book_ids(parsed_page):
    book_tags = parsed_page.select("div.bookimage a")
    id_tags = [tag.get('href') for tag in book_tags]
    return id_tags

def write_json(parsed_book_page):
    books = json.dumps(parsed_book_page, ensure_ascii = False).encode('utf8')
    with open("books.json", "w") as my_file:
        my_file.write(books.decode())



def main():
    parser = argparse.ArgumentParser(
        description = 'Script downloads books')
    parser.add_argument('--start_page', help = "Стартовая страница", default=1, type=int)
    parser.add_argument('--end_page', help = 'Финишная страница', default=701, type=int)
    parser.add_argument('--dest_folder', help = 'Путь к каталогу с картинками, книгами, JSON.', action="store_true", default=False)
    parser.add_argument('--skip_img', help = 'Не скачивать картинки', action="store_true", default=False)
    parser.add_argument('--skip_text', help = 'Не скачивать текст', action="store_true", default=False)
    args = parser.parse_args()

    book_pages = []
    for num in range(args.start_page, args.end_page, 1):
        book_ids = parse_book_ids(get_book_page(f'https://tululu.org/l55/{num}'))
        try:
            for book_id in book_ids:
                text_payload = {'id':'{}'.format(book_id.strip('/b'))}
                book_path = os.path.join('https://tululu.org/', book_id.strip('/'))
                book_page = script.parse_page(get_book_page(book_path))
                book_title = book_page['title']
                book_image = book_page['image']
                book_pages.append(book_page)
                if args.skip_img:
                    script.download_txt(text_payload, book_title)
                elif args.skip_text:
                    script.download_image(book_path, book_image)
                else:
                    script.download_txt(text_payload, book_title)
                    script.download_image(book_path, book_image)
        except requests.HTTPError:
            print("Книга не найдена. Введите другой id", file=sys.stderr)
    write_json(book_pages)
    if args.dest_folder:
        print(os.getcwd())
            
if __name__=='__main__':
    main()