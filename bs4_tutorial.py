import requests
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://tululu.org/b1/'
response = requests.get(url, verify=False, allow_redirects=False)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('h1')
title_text = title_tag.text
splited_text = title_text.split('::')
title = splited_text[0].rstrip(' \xa0')
author = splited_text[1].rstrip(' \xa0')
print('Заголовок: ', title)
print('Автор: ', author)


