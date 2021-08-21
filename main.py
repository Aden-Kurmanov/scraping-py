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

url = 'https://www.superjob.ru/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}

jobs_list = []

for i in range(search_pages):
    print('index: ', i)
    params = {
        'keywords': search_position
    }

    if i > 0:
        params['page'] = i

    response = requests.get(f"{url}/vacancy/search/", params=params, headers=headers)

    soup = bs(response.text, 'html.parser')
    main = soup.find_all('div', attrs={'class': '_3zucV _3rq8C _1b_NL'})[1]
    blocks = main.find_all('div', attrs={'class', 'f-test-vacancy-item'})

    for block in blocks:
        obj_data = {}
        link_salary_block = block.find('div', attrs={'class', 'jNMYr GPKTZ _1tH7S'})
        obj_data['name'] = link_salary_block.find('a', attrs={'class', 'icMQ_'}).getText()
        main_salary_block = link_salary_block.find('span', attrs={'class', 'f-test-text-company-item-salary'})
        # print(obj_data['name'])
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
                    min_s_common = str(salary_list[len(salary_list) - 1])

                    min_s = ''
                    currency = ''

                    for s in min_s_common:
                        try:
                            s = int(s)
                            min_s += str(s)
                        except:
                            currency += s

                    min_s = int(min_s)

                    obj_data['min_salary'] = min_s
                    obj_data['max_salary'] = None
                    obj_data['currency'] = currency
                # else:
                #     print(salary_list)
            # len_s = len(salary_block.findChildren(recursive=False))
            # if len_s == 0:
            #     min_s = salary_block.getText()
            #     print(obj_data['name'])
            #     print(min_s)
            #     obj_data['min_salary'] = ""
            #     obj_data['max_salary'] = None
            #     obj_data['currency'] = ""
            # elif len_s == 1:
            #     obj_data['min_salary'] = ""
            #     obj_data['max_salary'] = ""
            #     obj_data['currency'] = ""

        print('')
        # if salary_block.children == 0:
        #     print('salary chat: ', salary_block.getText())

        # obj_data['min_salary'] = link_salary_block.find('span', attrs={'class', '_1h3Zg'}).getText()
        jobs_list.append(obj_data)

p(jobs_list)

# for i in range(search_pages):
#     print('index: ', i)
#     url = 'https://hh.ru/'
#     params = {
#         'area': '159',
#         'fromSearchLine': 'true',
#         'st': 'searchVacancy',
#         'text': search_position
#     }
#
#     if i > 0:
#         params['page'] = i
#
#     # headers = {
#     #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
#     # }
#     # full_url = f"{url}/search/vacancy"
#     full_url = f"{url}/search/vacancy?area=159&fromSearchLine=true&st=searchVacancy&text={search_position}"
#
#     if i > 0:
#         full_url += f'&page={i}'
#
#     options = webdriver.ChromeOptions()
#     options.add_argument('User-Agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"')
#     browser = webdriver.Chrome(options=options)
#     browser.get(full_url)
#     soup = bs(browser.page_source, 'html.parser')
#     blocks = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
#     print(blocks)
#     browser.close()

# for i in range(search_pages):
#     print('index: ', i)
#     url = 'https://hh.ru/'
#     params = {
#         'area': '159',
#         'fromSearchLine': 'true',
#         'st': 'searchVacancy',
#         'text': search_position
#     }
#
#     if i > 0:
#         params['page'] = i
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
#     }
#
#     response = requests.get(f"{url}/search/vacancy", params=params, headers=headers)
#
#     soup = bs(response.text, 'html.parser')
#     blocks = soup.find('div', attrs={'class': 'vacancy-serp'})
#     print(blocks)




# for i in range(search_pages):
#     print('index: ', i)
#     url = 'https://hh.ru/'
#     params = {
#         'area': '159',
#         'fromSearchLine': 'true',
#         'st': 'searchVacancy',
#         'text': search_position
#     }
#
#     if i > 0:
#         params['page'] = i
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
#     }
#     full_url = f"{url}/search/vacancy"
#     # full_url = f"{url}/search/vacancy?area=159&fromSearchLine=true&st=searchVacancy&text={search_position}"
#
#     session = HTMLSession()
#
#     session.headers = headers
#     session.params = params
#
#     resp = session.get(full_url)
#     resp.html.render()
#     resp.close()
#
#     soup = bs(resp.text, 'html.parser')
#     blocks = soup.find_all('div', attrs={'class': 'vacancy-serp-item'})
#     print(blocks)


