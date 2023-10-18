# 네이버 쇼핑몰 크롤링_부분 테스트 version
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


from webdriver_manager.chrome import ChromeDriverManager

from openpyxl import Workbook
from openpyxl.styles import Alignment

import time
import csv
import random


# 브라우져 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach",True)

# 불필요한 에러 메시지 없애기
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())  # Chrome driver 자동 업데이트
driver = webdriver.Chrome(service=service, options=chrome_options)
# driver.maximize_window() #화면 최대화

# 해당 웹페이지로 이동
driver.get("https://datalab.naver.com/shoppingInsight/sCategory.naver")
driver.implicitly_wait(10)

randome_time = random.random()*1.2
total_lst = []

wb = Workbook()
ws = wb.create_sheet("카테고리 항목들 수집")

# 인기 검색어 대표 타이틀
def insite_title() :
    time.sleep(.4)
    return driver.find_element(By.CSS_SELECTOR, ".section .insite_title strong").text


# def dropdown_click(dropdown_arr):
#     dropdown_arr.click()
#     time.sleep(randome_time)



dropdowns = driver.find_elements(By.CSS_SELECTOR,".set_period.category  .select")
first_options = dropdowns[0].find_elements(By.CSS_SELECTOR,"li .option")

dropdowns[0].click()
time.sleep(.4)
first_options[0].click()
time.sleep(.4)

second_options = dropdowns[1].find_elements(By.CSS_SELECTOR,"li .option")
dropdowns[1].click()
time.sleep(.4)
second_options[1].click()
time.sleep(.4)

dropdowns = driver.find_elements(By.CSS_SELECTOR,".set_period.category  .select")
third_options = dropdowns[2].find_elements(By.CSS_SELECTOR,"li .option")
dropdowns[2].click()
time.sleep(.4)
third_options[4].click()
time.sleep(.4)

driver.find_elements(By.CSS_SELECTOR,".btn_submit")[0].click()
time.sleep(1)

total_lst.append(insite_title())

found_error = False # 2중 for문 break
for i in range(25) :  # 버튼이 25개
    ranks = driver.find_elements(By.CSS_SELECTOR, ".rank_top1000 .link_text")[3]
    
    
    text = ranks.text
    span = ranks.find_element(By.CSS_SELECTOR,".rank_top1000_num")
    text = text.replace(span.text, "").strip()
    total_lst.append(text)
    
    if found_error :
        break
    driver.find_element(By.CSS_SELECTOR, ".btn_page_next").click()


ws.append(total_lst)
wb.save(f"Category_search.xlsx")

print(total_lst)