import requests
from bs4 import BeautifulSoup
import openpyxl

wb = openpyxl.Workbook()
sheet = wb.active
sheet.append(["종목명","PER","ROE","PBR","유보율"])

response = requests.get(f"https://finance.naver.com/sise/sise_market_sum.naver")
html = response.text
soup = BeautifulSoup(html,"html.parser")

clicks_lst = [6,12,18,24,27]

new_lst = []
for click_lst in clicks_lst:
    new_lst.append(soup.select_one(f"input#option{click_lst}").attrs["value"])

page = 10

for i in range(1,page):
    # 여러개의 파라미터가 있으면 & 기호를 쓰는데 일반적으로는 ?로 시작
    # 만일 페이지가 잘 안넘어가면 ?&page 부분이 있나 확인 
    url = f"https://finance.naver.com/sise/field_submit.naver?menu=market_sum&returnUrl=http://finance.naver.com/sise/sise_market_sum.naver?page={i}&fieldIds={new_lst[0]}&fieldIds={new_lst[1]}&fieldIds={new_lst[2]}&fieldIds={new_lst[3]}&fieldIds={new_lst[4]}"
    response = requests.get(url, headers= {"User-Agent": "Mozilla/5.0"})
    html = response.text
    soup = BeautifulSoup(html,"html.parser")

    table = soup.select_one(".type_2>tbody")
    # 일반적인 태그말고 특성도 지징할 때
    trs = table.select("tr[onmouseover='mouseOver(this)']")  # 따옴표안에 또 따옴표 넣을 경우 다른 형태로 

    for idx,tr in enumerate(trs,1):
        title = tr.select_one("td:nth-of-type(2)").text
        per = tr.select_one("td:nth-of-type(7)").text
        roa = tr.select_one("td:nth-of-type(9)").text
        pbr = tr.select_one("td:nth-of-type(10)").text
        reserve_ratio = tr.select_one("td:nth-of-type(11)").text

        if per != 'N/A' and roa != 'N/A' and pbr != 'N/A' and  reserve_ratio != 'N/A' :
            per = float(per.replace(",",""))
            roa = float(roa.replace(",",""))
            pbr = float(pbr.replace(",",""))
            reserve_ratio = float(reserve_ratio.replace(",",""))
            sheet.append([title,per,roa,pbr,reserve_ratio])
            print(f"{title} : {per} | {roa} | {pbr} | {reserve_ratio}")
        
wb.save("시가총액.csv")


