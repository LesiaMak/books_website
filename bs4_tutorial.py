import requests
import urllib3
from bs4 import BeautifulSoup
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = 'https://tululu.org/b9/'
response = requests.get(url, verify=False, allow_redirects=False)
response.raise_for_status()
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('table', class_='tabs').find('td', class_='ow_px_td').find('h1')
image_link = soup.find('div', class_='bookimage').find('img')['src']
genres = soup.find('span', class_='d_book').find_all('a')
for genre in genres:
	print(genre.text)
comments = soup.find_all('div', {'class': 'texts'})
for comment in comments:
	comment_text = comment.text
	splited_comment = comment_text.split(')')
	#print(splited_comment[-1])
title_text = title_tag.text
splited_text = title_text.split('::')
title = splited_text[0].rstrip(' \xa0')
author = splited_text[1].rstrip(' \xa0')
#print('Заголовок: ', title)
#print('Автор: ', author)
#print(image_link)


