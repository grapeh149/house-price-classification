from numpy.random import normal
from selenium.webdriver.chrome.options import Options

from numpy.f2py.crackfortran import n
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import pandas as pd
# from Preprocesing import *

from time import sleep



path = "D:\Data Analyst Project\housing-price-classification\data\data_raw"

data = pd.DataFrame({"P": ["Alice"], 'area': [234], 'pam': [234], 'bed': [4], 'Tolet': [5], 'Address': ['dads'],
                     'Home Direction': ['aaa'],
                     'Facade': ['bbbb'], 'Access': [2], 'Papers': ['123'], 'Interior': ['122'],
                     'Balcony view': ['hsids']})
data.columns = ["Price", "Area", "Bedroom", "Toilet, Bathroom", "Floor", "Home Direction", "Facade", "Access", "Papers",
                "Interior", "Balcony view", "Address"]
print(data)

chrome_options = Options()

chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--start-maximized")
browers = uc.Chrome(
    options=chrome_options,
    use_subprocess=True
)
browers.get("https://batdongsan.com.vn/ban-can-ho-chung-cu-quan-1?cIds=41,325,163")
sleep(2)
p = 2

for _ in range(41):

    count = browers.find_element(By.ID, "product-lists-web")
    cards = count.find_elements(By.CLASS_NAME, "js__card.js__card-full-web.pr-container.re__card-full")
    print(f'Scraping data on this page {p - 1}....')
    for item in cards:
        k = item.find_element(By.CLASS_NAME, "js__product-link-for-product-id")
        old_tab = browers.current_window_handle
        browers.execute_script(f"window.open('{k.get_attribute('href')}','_blank');")
        new_window = browers.window_handles[-1]
        browers.switch_to.window(new_window)

        report = browers.find_element(By.CLASS_NAME, "re__pr-info.pr-info.js__product-detail-web")
        address = browers.find_element(By.CLASS_NAME, "re__pr-short-description.js__pr-address")
        features = report.find_element(By.CLASS_NAME, "re__pr-other-info-display")
        detail = features.find_elements(By.CLASS_NAME, "re__pr-specs-content-item")
        arr = []

        attributes = ["Mức giá", "Diện tích", "Số phòng ngủ", "Số phòng tắm, vệ sinh",
                      "Số tầng", "Hướng nhà", "Mặt tiền", "Đường vào",
                      "Pháp lý", "Nội thất", "Hướng ban công"]

        data_dict = {attr: None for attr in attributes}

        for k in detail:
            key = k.find_element(By.CLASS_NAME, "re__pr-specs-content-item-title").text
            value = k.find_element(By.CLASS_NAME, "re__pr-specs-content-item-value").text

            if key in data_dict:
                data_dict[key] = value

        arr = [data_dict[attr] for attr in attributes]
        arr.append(address.text)

        sleep(2)
        browers.close()
        browers.switch_to.window(old_tab)
        data.loc[len(data)] = arr



    path = f'https://batdongsan.com.vn/ban-can-ho-chung-cu-quan-1/p{p}?cIds=41,325,163'
    p += 1
    browers.get(path)
    sleep(4)

print(data)

# print(data)
district = "6"
data.to_excel(f'{path}\\data_Quan{district}.csv')
sleep(3)
browers.quit()


