import requests
import urllib3
import os
from bs4 import BeautifulSoup
from pathvalidate import sanitize_filepath


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
    filename = sanitize_filepath(os.path.join(folder, filename + '.txt'))
    return filename

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

for i in range(1, 10):
    try:
        title_url = 'https://tululu.org/b{}/'.format(i)
        print(title_url)
        txt_url = 'https://tululu.org/txt.php?id={}'.format(i)
        print(txt_url)
        title = get_title(title_url)
        print(title)
        responce = check_for_redirect(txt_url)
        filename = download_txt(txt_url, title)
        with open(filename, 'w') as file:
            file.write(responce.text)
    except requests.HTTPError:
        pass









