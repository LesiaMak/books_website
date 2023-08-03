import requests
import urllib3
import os
import sys
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
import argparse
import time



urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_for_redirect(response):
    if response.history:
        raise requests.exceptions.HTTPError 



def download_txt(payload, filename, folder="books"):
    os.makedirs(os.path.join('./',folder), exist_ok=True)    
    response = requests.get('https://tululu.org/txt.php', params=payload, verify=False, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    book_filepath = sanitize_filepath(os.path.join(folder, f'{filename}.txt'))
    with open(book_filepath, 'w') as file:
        file.write(response.text)
    


def download_image(url, image_url, folder="images"):
    os.makedirs(os.path.join('./',folder), exist_ok=True)
    image_link = urljoin(url, image_url)
    splited_link =image_link.split('/')
    image_name = splited_link[-1]
    image_filepath = sanitize_filepath(os.path.join(folder, image_name))
    response = requests.get(image_link, verify=False, allow_redirects=True)
    response.raise_for_status()
    check_for_redirect(response)
    with open(image_filepath, 'wb') as file:
         file.write(response.content)
    


def download_comments(title, comments):
    filename = 'books/comments_{}'.format(title)
    joined_comments = " ".join(map(str, comments))
    with open(filename, 'w') as file:
        file.write(joined_comments)
    return joined_comments


def parse_page(parsed_page):
    title_tag = parsed_page.select_one(".tabs .ow_px_td h1")
    title_text = title_tag.text
    splited_text = title_text.split('::')
    author = splited_text[1].strip(' \xa0')
    title = splited_text[0].rstrip(' \xa0')
    image_selector = parsed_page.select_one(".ow_px_td .bookimage img")
    image_url = image_selector.get('src')
    comments = parsed_page.find_all('div', {'class': 'texts'})
    all_comments = []
    for comment in comments:
        comments_text = comment.text
        splited_comments = comments_text.split(')')
        actual_comments = splited_comments[-1]
        all_comments.append(actual_comments)
    genres = parsed_page.select('span.d_book a')    
    book_genres = [genre.text for genre in genres]
    page = {
        'title': title,
        'author': author,
        'genre': book_genres,
        'comments': all_comments,
        'image': image_url,
        }
    return page
    

def get_book_page(url):
    response = requests.get(url, verify=False, allow_redirects=True)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    return soup

    

def main():
    parser = argparse.ArgumentParser(
        description = 'Script downloads books')
    parser.add_argument('start_id', help = "Стартовое id", default=1, type=int)
    parser.add_argument('end_id', help = 'Финишное id', default=10, type=int)
    args = parser.parse_args()

    for num in range(args.start_id, args.end_id):
        try:
            text_payload = {'id':'{}'.format(num)}
            title_url = 'https://tululu.org/b{}/'.format(num)
            book_page = parse_page(get_book_page(title_url))
            book_title = book_page['title']
            book_image = book_page['image']
            book_comments = book_page['comments']
            download_txt(text_payload, book_title)
            download_image(title_url, book_image)
            download_comments(book_title, book_comments)
        except requests.HTTPError:
            print("Книга не найдена. Введите другой id", file=sys.stderr)
        except requests.ConnectionError:
            print('Нет связи с сервером', file=sys.stderr)
            time.sleep(5)

          

if __name__=='__main__':
    main()








