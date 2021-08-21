from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint as p

search_position = input('Введите должность: ')
search_pages = input('На скольких страницах искать: ')

is_not_num = True
while is_not_num:
    try:
        search_pages = int(search_pages)
        is_not_num = False
    except:
        print()
        print('Требуется ввести число!')
        search_pages = input('На скольких страницах искать: ')


for i in range(search_pages):
    print('index: ', i)
    url = 'https://hh.ru/'
    params = {
        'area': '159',
        'fromSearchLine': 'true',
        'st': 'searchVacancy',
        'text': search_position
    }

    if i > 0:
        params['page'] = i

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
    }

    response = requests.get(f"{url}/search/vacancy", params=params, headers=headers)

    soup = bs(response.text, 'html.parser')
    blocks = soup.find('div', attrs={'class': 'bloko-gap'})
    print(blocks)


