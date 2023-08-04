import requests
import urllib3
import os
import sys
import time
from urllib.parse import urljoin
import parse_tululu_books
import json
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def parse_book_links(parsed_page):
    book_tags = parsed_page.select("div.bookimage a")
    book_links = [tag.get('href') for tag in book_tags]
    return book_links

def write_json(parsed_book_page):
    with open("books.json", "w") as file:
        json.dump(parsed_book_page, file, indent=4, separators=(", ", ": "), ensure_ascii=False)



def main():
    parser = argparse.ArgumentParser(
        description = 'Script downloads books')
    parser.add_argument('--start_page', help = "Стартовая страница", default=1, type=int)
    parser.add_argument('--end_page', help = 'Финишная страница', default=701, type=int)
    parser.add_argument('--skip_img', help = 'Не скачивать картинки', action="store_true", default=False)
    parser.add_argument('--skip_text', help = 'Не скачивать текст', action="store_true", default=False)
    parser.add_argument('--dest_folder', help = 'Путь к каталогу с картинками, книгами, JSON.', action="store_true", default=False)
    args = parser.parse_args()

    book_pages = []
    try:
        for num in range(args.start_page, args.end_page, 1):
            try:
                book_links = parse_book_links(parse_tululu_books.get_book_page(f'https://tululu.org/l55/{num}'))
            except requests.exceptions.ConnectionError:
                print('Нет связи с сервером', file=sys.stderr)
                for book_link in book_links:
                    try:
                        text_payload = {'id':'{}'.format(book_link.strip('/b'))}
                        book_path = (f'https://tululu.org{book_link}')
                        book_page = parse_tululu_books.parse_page(parse_tululu_books.get_book_page(book_path))
                        book_title = book_page['title']
                        book_image = book_page['image']
                        book_pages.append(book_page)                    
                        if args.skip_img: parse_tululu_books.download_txt(text_payload, book_title) 
                        else: parse_tululu_books.download_image(book_path, book_image)
                        if args.skip_text: parse_tululu_books.download_image(book_path, book_image)
                        else: parse_tululu_books.download_txt(text_payload, book_title)
                    except requests.HTTPError:
                        print("Книга не найдена. Введите другой id", file=sys.stderr)
                    except requests.exceptions.ConnectionError:
                        print('Нет связи с сервером', file=sys.stderr)
                        time.sleep(5)
        write_json(book_pages)
        if args.dest_folder:
            print(os.getcwd())
    except requests.exceptions.ConnectionError:
        print('Нет связи с сервером', file=sys.stderr)
        time.sleep(5)

            
if __name__=='__main__':
    main()