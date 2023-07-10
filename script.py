import requests
import urllib3
import os
import sys
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
import urllib.request
import argparse


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def check_for_redirect(response):
    try:
        response.raise_for_status()
        return response
    except requests.HTTPError:
        raise('Book havent found')


def download_txt(payload, filename, folder="books"):
    os.makedirs(os.path.join('./',folder), exist_ok=True)
    book_filename = sanitize_filepath(os.path.join(folder, filename + '.txt'))
    response = requests.get('https://tululu.org/txt.php', params=payload, verify=False, allow_redirects=False)
    check_for_redirect(response)
    with open(book_filename, 'w') as file:
        file.write(response.text)
    return filename


def download_image(url, image_link, folder="images"):
    os.makedirs(os.path.join('./',folder), exist_ok=True)
    splited_link =image_link.split('/')
    image_name = splited_link[-1]
    filename = sanitize_filepath(os.path.join(folder, image_name))
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)
    with open(filename, 'wb') as file:
         file.write(response.content)
    return filename


def download_comments(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)
    filename = 'books/comments_{}'.format(get_page(parse_book_page(url))['Title'])
    comments = " ".join(map(str, get_page(parse_book_page(url))['Comments']))
    with open(filename, 'w') as file:
        file.write(comments)
    return response


def get_page(parsed_page):
    title_tag = parsed_page.find('table', class_='tabs').find('td', class_='ow_px_td').find('h1')
    title_text = title_tag.text
    splited_text = title_text.split('::')
    author = splited_text[1].strip(' \xa0')
    title = splited_text[0].rstrip(' \xa0')
    image_tag = parsed_page.find('div', class_='bookimage').find('img')['src']
    image_link = urljoin('tululu.org',image_tag)
    comments = parsed_page.find_all('div', {'class': 'texts'})
    all_comments = []
    for comment in comments:
        comments_text = comment.text
        splited_comments = comments_text.split(')')
        actual_comments = splited_comments[-1]
        all_comments.append(actual_comments)
    genres = parsed_page.find('span', class_='d_book').find_all('a')
    book_genres = [genre.text for genre in genres]
    page = {
        'Title': title,
        'Author': author,
        'Genre': book_genres,
        'Image link': image_link,
        'Comments': all_comments
        }
    return page
    

def parse_book_page(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    check_for_redirect(response)
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
            text_url ='https://tululu.org/txt.php'
            payload_url = {'id':'{}'.format(num)}
            title_url = 'https://tululu.org/b{}/'.format(num)
            book = download_txt(payload_url, get_page(parse_book_page(title_url))['Title'])
            image = download_image(title_url, get_page(parse_book_page(title_url))['Image link'])
            comments = download_comments(title_url)
        except requests.HTTPError:
            print("Книга не найдена. Введите другой id", file=sys.stderr)
        except requests.ConnectionError:
            print('Нет связи с сервером', file=sys.stderr)

            

if __name__=='__main__':
    main()








