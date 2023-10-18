# 네이버지도 크롤링  (정석)
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

import time
import csv
import requests
from bs4 import BeautifulSoup
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["순위","이름","별점","방문자 리뷰","실제 리뷰"])

chrome_options = Options()
chrome_options.add_experimental_option("detach",True)
service = Service(executable_path=ChromeDriverManager().install())  # Chrome driver 자동 업데이트

browser = webdriver.Chrome(service=service, options=chrome_options)

browser.get("https://map.naver.com")
browser.implicitly_wait(10)

search = browser.find_element(By.CSS_SELECTOR,"input.input_search")
search.click()
time.sleep(1)
search.send_keys("군산 맛집")
time.sleep(1)
search.send_keys(Keys.ENTER)
time.sleep(2)

# iframe 안으로 들어가기
browser.switch_to.frame('searchIframe')

# browser.switch_to.default_content()  - iframe 밖으로 나오기

# 빈 공간 클릭
browser.find_element(By.CSS_SELECTOR,"#_pcmap_list_scroll_container").click()

contents= browser.find_elements(By.CSS_SELECTOR,"li.UEzoS.rTjJo")

# 무한 스크롤 (스크롤 높이로 안될때)
before_len = len(contents)
while True:
    # 맨 아래로 스크롤 내린다
    browser.find_element(By.CSS_SELECTOR,"body").send_keys(Keys.END)
    time.sleep(1)

    contents= browser.find_elements(By.CSS_SELECTOR,"li.UEzoS.rTjJo")
    after_len = len(contents)

    if  before_len == after_len:
        break
    before_len = after_len


browser.implicitly_wait(3) # 데이터 없으면 빠르게 넘어감

rank = 1

for content in contents:
    # 목록 프레임으로 이동
    browser.switch_to.default_content()
    browser.switch_to.frame('searchIframe')

    # if문으로 광고 상품 제거
    if (len(content.find_elements(By.CSS_SELECTOR,'svg.dPXjn'))==0):
        name = content.find_element(By.CSS_SELECTOR,"span.place_bluelink")
        name.click()
        time.sleep(0.3)

        # 상세 프레임으로 이동
        browser.switch_to.default_content()
        browser.switch_to.frame('entryIframe')

        title = browser.find_element(By.CSS_SELECTOR,"div.YouOG").text

        lsts = browser.find_elements(By.CSS_SELECTOR,"span.PXMot")
        if (len(lsts) == 2):
            try:
                real_view = browser.find_element(By.CSS_SELECTOR,"div.dAsGb>span:nth-of-type(1)>a>em").text
            except :
                print("방문자 0명")
            try :
                blog_view = browser.find_element(By.CSS_SELECTOR,"div.dAsGb>span:nth-of-type(2)>a>em").text
            except :
                print("블로그 후기 0명")
        elif (len(lsts) == 3) :
            star = browser.find_element(By.CSS_SELECTOR,"div.dAsGb>span:nth-of-type(1)>em").text
            try:
                real_view = browser.find_element(By.CSS_SELECTOR,"div.dAsGb>span:nth-of-type(2)>a>em").text
            except :
                print("방문자 0명")
            try :
                blog_view = browser.find_element(By.CSS_SELECTOR,"div.dAsGb>span:nth-of-type(3)>a>em").text
            except :
                print("블로그 후기 0명")

        real_view = int(real_view.replace(",",""))
        blog_view = int(blog_view.replace(",",""))
        if (star):
            sheet.append([rank,title,float(star),real_view,blog_view])    
        else:
            sheet.append([rank,title," ",real_view,blog_view])
            
        time.sleep(0.3)

        rank += 1

# 여기에서 활성화 시트를 저장하는게 아니라 workbook을 저장해야한다.
wb.save("네이버지도크롤링.csv")





