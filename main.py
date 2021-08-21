from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint as p
import json

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

url = 'https://www.superjob.ru'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}


def get_salary_currency(string):
    m = ''
    c = ''

    for s in string:
        try:
            s = int(s)
            m += str(s)
        except:
            c += s

    return int(m), c


jobs_list = []

for i in range(search_pages):
    params = {
        'keywords': search_position
    }

    if i > 0:
        params['page'] = i

    response = requests.get(f"{url}/vacancy/search/", params=params, headers=headers)

    soup = bs(response.text, 'html.parser')
    all_found = soup.find_all('div', attrs={'class': '_3zucV _3rq8C _1b_NL'})
    if len(all_found) == 1:
        break
    main = all_found[1]
    blocks = main.find_all('div', attrs={'class', 'f-test-vacancy-item'})

    for block in blocks:
        obj_data = {}
        link_salary_block = block.find('div', attrs={'class', 'jNMYr GPKTZ _1tH7S'})
        a_block = link_salary_block.find('a', attrs={'class', 'icMQ_'})
        obj_data['name'] = a_block.getText()
        obj_data['link'] = url + a_block['href']
        loc_block = block.find('span', attrs={'class', 'f-test-text-company-item-location'})
        loc_children = loc_block.findChildren(recursive=False)
        obj_data['address'] = str(loc_children[len(loc_children) - 1].getText()).replace('\xa0', ' ')
        main_salary_block = link_salary_block.find('span', attrs={'class', 'f-test-text-company-item-salary'})
        if len(main_salary_block.findChildren(recursive=False)) == 1:
            obj_data['min_salary'] = 'По договоренности'
            obj_data['max_salary'] = None
            obj_data['currency'] = None
        elif len(main_salary_block.findChildren(recursive=False)) == 2:
            salary_block = main_salary_block.find('span', attrs={'class', '_1h3Zg'})
            salary_list = [str(x).replace('\xa0', '').replace(' ', '') for x in list(salary_block.children)]
            vilka = [x for x in salary_list if x.find('<span') != -1]
            if len(vilka) > 0:
                v_list = [x for x in salary_list if x.find('<span') == -1]
                obj_data['currency'] = v_list[len(v_list) - 1]
                obj_data['min_salary'] = v_list[0]
                obj_data['max_salary'] = v_list[1]
            else:
                is_from = len([x for x in salary_list if x == 'от']) > 0
                if is_from:
                    min_s, currency = get_salary_currency(str(salary_list[len(salary_list) - 1]))

                    obj_data['min_salary'] = min_s
                    obj_data['max_salary'] = None
                    obj_data['currency'] = currency
                else:
                    is_to = len([x for x in salary_list if x == 'до']) > 0
                    if is_to:
                        max_s, currency = get_salary_currency(str(salary_list[len(salary_list) - 1]))
                        obj_data['min_salary'] = None
                        obj_data['max_salary'] = max_s
                        obj_data['currency'] = currency
                    else:
                        obj_data['min_salary'] = int(salary_list[0])
                        obj_data['max_salary'] = int(salary_list[0])
                        obj_data['currency'] = salary_list[len(salary_list) - 1]

        jobs_list.append(obj_data)

p(jobs_list)

with open('jobs.json', 'w', encoding="utf-8") as file:
    json.dump(jobs_list, file, ensure_ascii=False)

