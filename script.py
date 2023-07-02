import requests
import urllib3
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin
import argparse

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def check_for_redirect(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 200:
        return response
    else:
        raise requests.HTTPError("Book havent found")


def download_txt(url, filename, folder="books"):
    os.makedirs(os.path.join('D:/Python/books_website/',folder), exist_ok=True)
    book_filename = sanitize_filepath(os.path.join(folder, filename + '.txt'))
    response = check_for_redirect(url)
    with open(book_filename, 'w') as file:
        file.write(response.text)
    return filename


def download_image(url, image_link, folder="images"):
    os.makedirs(os.path.join('D:/Python/books_website/',folder), exist_ok=True)
    splited_link =image_link.split('/')
    image_name = splited_link[-1]
    filename = sanitize_filepath(os.path.join(folder, image_name))
    response = check_for_redirect(url)
    with open(filename, 'wb') as file:
        file.write(response.content)
    return filename


def download_comments(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    filename = 'books/comments_{}'.format(parse_book_page(url)['Заголовок'])
    with open(filename, 'w') as file:
        file.write(parse_book_page(url)['Комментарии'])
    return response


def parse_book_page(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('h1')
        title_text = title_tag.text
        splited_text = title_text.split('::')
        author = splited_text[1].strip(' \xa0')
        title = splited_text[0].rstrip(' \xa0')
        image_tag = soup.find('div', class_='bookimage').find('img')['src']
        image_link = urljoin('https://tululu.org/',image_tag)
        comments = soup.find_all('div', {'class': 'texts'})
        all_comments = []
        for comment in comments:
            comments_text = comment.text
            splited_comments = comments_text.split(')')
            actual_comments = splited_comments[-1]
            all_comments.append(actual_comments)
        book_genre =[] 
        genres = soup.find('span', class_='d_book').find_all('a')
        for genre in genres:
            book_genre.append(genre.text)
        page = {
            'Заголовок': title,
            'Автор': author,
            'Жанр': book_genre,
            'Image link': image_link,
            'Комментарии': all_comments
            }
        return page
    else:
        raise requests.HTTPError("Book havent found")


parser = argparse.ArgumentParser(
    description = 'Script downloads books')
parser.add_argument('start_id', help = "Стартовое id", default=1, type=int)
parser.add_argument('end_id', help = 'Финишное id', default=10, type=int)
args = parser.parse_args()

for i in range(args.start_id, args.end_id):
    try:
        title_url = 'https://tululu.org/b{}/'.format(i)
        txt_url = 'https://tululu.org/txt.php?id={}'.format(i)
        title = parse_book_page(title_url)['Заголовок']
        author = parse_book_page(title_url)['Автор']
        print('Зоголовок: ', title)
        print('Автор: ', author)
        book = download_txt(txt_url, title)
    except requests.HTTPError:
        pass









