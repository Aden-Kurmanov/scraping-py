from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
from selenium import webdriver
import time
from pprint import pprint as p
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SE

client = MongoClient("127.0.0.1", 27017)

db = client['geekBrains_data_from_net']

posts = db.posts

chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)

driver.get("https://mail.ru/")

#  Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и
#  сложить данные о письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
# Логин тестового ящика: study.ai_172@mail.ru
# Пароль тестового ящика: NextPassword172???

form = driver.find_element_by_xpath("//form[@data-testid='logged-out-form']")
login = form.find_element_by_xpath("//input[contains(@class, 'email-input')]")
login.send_keys('study.ai_172')
btn_enter_pass = form.find_element_by_xpath("//button[@data-testid='enter-password']")
btn_enter_pass.click()
print()

wait = WebDriverWait(form, 10)

time.sleep(1)
password = form.find_element_by_xpath("//input[@data-testid='password-input']")
password.send_keys('NextPassword172???')

btn_to_mail = form.find_element_by_xpath("//button[@data-testid='login-to-mail']")
btn_to_mail.click()











# driver.get("https://www.mvideo.ru/")

#
# new_products = db.new_products
#
# chrome_options = Options()
# chrome_options.add_argument('start-maximized')
# prefs = {"profile.default_content_setting_values.notifications" : 2}
# chrome_options.add_experimental_option("prefs", prefs)
#
# driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)
#
# driver.get("https://www.mvideo.ru/")
#
# actions = ActionChains(driver)
# actions.move_by_offset(10, 10).click()
# actions.perform()
#
# geolocation_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'geolocation__action-approve-city')]")))
# geolocation_btn.click()
#
# time.sleep(0.5)
#
# news_section = driver.find_element_by_xpath("//h2[contains(text(), 'Новинки')]/../../../div[contains(@class, 'gallery-content')]//div[contains(@class, 'accessories-carousel-wrapper')]")
# scroll_to_element = ActionChains(driver)
# scroll_to_element.move_to_element(news_section)
#
# goods_list = []
# goods_path = "//li[@class='gallery-list-item']/div[contains(@class, 'fl-product-tile')]"
#
# scroll_to_element.perform()
#
# while True:
#     wait = WebDriverWait(news_section, 10)
#     try:
#         goods_list = goods_list.extend(news_section.find_elements_by_xpath(goods_path))
#         next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'next-btn')]")))
#         next_btn.click()
#     except Exception as e:
#         print("exception: ", e)
#         break



# for good in goods_list:
#     print("good: ", good)

# content = driver.fin

# for i in range(5):
#     actions = ActionChains(driver)
#     articles = driver.find_element_by_tag_name('article')
#     actions.move_to_element(articles[-1]).perform()
#     time.sleep(3)
#
# driver.execute_script("")

# actions = ActionChains(driver)
# actions.move_by_offset(100, 100).click()
# actions.perform()
#
# time.sleep(0.5)
# btn_cookie = driver.find_element_by_class_name('cookie-usage-notice__button')
# btn_cookie.click()
# time.sleep(0.5)
# page = 0
# class_name = "//button[@class='button button--primary catalog-grid-container__pagination-button']"
# while page < 2:
#     wait = WebDriverWait(driver, 10)
#     try:
#         btn_wait = wait.until(EC.presence_of_element_located((By.XPATH, class_name)))
#         btn_wait.click()
#         page += 1
#     except SE.TimeoutException:
#         break
#
# goods = driver.find_elements_by_class_name('sku-card-small-container')
# for good in goods:
#     print(good.find_element_by_class_name('sku-card-small__title').text)

# close = driver.find_element_by_class_name('close-control')
# close.click()



# login = driver.find_element_by_id('user_email')
# login.send_keys('aden.kurmanov@mail.ru')
#
# password = driver.find_element_by_id('user_password')
# password.send_keys('Wikipedia1')
# password.send_keys(Keys.ENTER)
#
# menu = driver.find_element_by_xpath("//span[contains(text(), 'меню')]")
# menu.click()
#
# button = driver.find_element_by_xpath("//button[@data-test-id='user_dropdown_menu']")
# button.click()
#
# link = driver.find_element_by_xpath("//li/a[contains(@href, '/users/')]")
# url = link.get_attribute('href')
# driver.get(url)
# client = MongoClient("127.0.0.1", 27017)
# db = client['geekBrains_data_from_net']
# news = db.news

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
# }
