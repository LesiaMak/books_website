import requests
import urllib3
import os

os.makedirs('D:/Python/books_website/books', exist_ok=True)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
for i in range(10):
    url = 'https://tululu.org/txt.php?id=3216{}'.format(i)
    response = requests.get(url, verify=False)
    response.raise_for_status()
    filename = 'books/{}.txt'.format(i)
    with open(filename, 'w') as file:
        file.write(response.text)

