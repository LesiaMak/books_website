import requests
import urllib3
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath
from urllib.parse import urljoin

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



def get_image_link(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        image_tag = soup.find('div', class_='bookimage').find('img')['src']
        image_link = urljoin('https://tululu.org/',image_tag)
        return image_link
    else:
        raise requests.HTTPError("Image havent found")


def get_title(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        title_tag = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('h1')
        title_text = title_tag.text
        splited_text = title_text.split('::')
        title = splited_text[0].rstrip(' \xa0')        
        return title
    else:
        raise requests.HTTPError("Book havent found")

def get_comments(url):
    response = requests.get(url, verify=False, allow_redirects=False)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'lxml')
    comments = soup.find_all('div', {'class': 'texts'})
    for comment in comments:
        comments_text = comment.text
        splited_comments = comments_text.split(')')
        actual_comments = splited_comments[-1]
        filename = 'books/comments_{}'.format(get_title(url))
        with open(filename, 'w') as file:
            file.write(actual_comments)
    return response

for i in range(1, 10):
    try:
        title_url = 'https://tululu.org/b{}/'.format(i)
        txt_url = 'https://tululu.org/txt.php?id={}'.format(i)
        comments = get_comments(title_url)
        print(comments)
    except requests.HTTPError:
        pass









