from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import selenium.common.exceptions as SE
from pymongo import MongoClient
from selenium import webdriver
import time
import ast

client = MongoClient("127.0.0.1", 27017)

db = client['geekBrains_data_from_net']

posts = db.posts

chrome_options = Options()
chrome_options.add_argument('start-maximized')
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)

url = "https://www.mvideo.ru/"
driver.get(url)

new_products = db.new_products
time.sleep(2)

geolocation_btn = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'geolocation__action-approve-city')]")))

actions = ActionChains(driver)
actions.move_by_offset(10, 10).click()
actions.perform()

main_xpath = "//h2[contains(text(), 'Новинки')]/../../../div[contains(@class, 'gallery-content')]//div[contains(@class, 'accessories-carousel-wrapper')]"
news_section = driver.find_element_by_xpath(main_xpath)
driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().y)", news_section)

while True:
    try:
        next_btn = WebDriverWait(driver, 7).until(EC.element_to_be_clickable((By.XPATH, f"{main_xpath}//a[contains(@class, 'next-btn')]")))
        next_btn.click()
    except SE.ElementClickInterceptedException:
        goods_list = news_section.find_elements_by_class_name('gallery-list-item')
        break
    except SE.TimeoutException:
        goods_list = news_section.find_elements_by_class_name('gallery-list-item')
        break

for good in goods_list:
    a = good.find_element_by_xpath(".//a[contains(@class, 'fl-product-tile-title__link')]")
    is_exists = False
    info = ast.literal_eval(a.get_attribute("data-product-info"))
    info['link'] = a.get_attribute("href")

    for _ in posts.find({'link': info['link']}):
        is_exists = True
        break

    if is_exists:
        continue

    info["productPriceLocal"] = float(info["productPriceLocal"])
    posts.insert_one(info)

for item in posts.find({}):
    print(item)
