# 키워드 분석_version(1.0)
import time
import requests
import signaturehelper

def get_header(method, uri, api_key, secret_key, customer_id):
    timestamp = str(round(time.time() * 1000))
    signature = signaturehelper.Signature.generate(timestamp, method, uri, SECRET_KEY)
    return {'Content-Type': 'application/json; charset=UTF-8', 
            'X-Timestamp': timestamp,
            'X-API-KEY': API_KEY, 
            'X-Customer': str(CUSTOMER_ID),
            'X-Signature': signature}

API_KEY = '01000000004031c42277f90c7fdcbd2130a4916b0aecf181b89b3543abab0f90b463c42821'
SECRET_KEY = 'AQAAAABAMcQid/kMf9y9ITCkkWsKnGbFkehYuYSpmb3ygOH/tg=='
CUSTOMER_ID = '3003237'
BASE_URL =  'https://api.naver.com'



# Sample
uri = '/keywordstool'
method = 'GET'
query = {
    "siteId" : "",
    "biztpId" : "",
    "hintKeywords": "누텔라",
    "event": "",
    "month": "",
    "showDetail": "1"
}

response = requests.get(BASE_URL + uri ,
                        params=query, 
                        headers=get_header(
                            method=method,
                            uri=uri,
                            api_key= API_KEY,
                            secret_key= SECRET_KEY,
                            customer_id= CUSTOMER_ID))

r_data = response.json()


keywordList = r_data['keywordList']
print("관련 키: ", keywordList[0]['relKeyword'] )
print("월간 검색수_PC: ",keywordList[0]['monthlyPcQcCnt'] )
print("월간 검색수_Mobile: ",keywordList[0]['monthlyMobileQcCnt'] )
print("월 평균 클릭수_PC: ",keywordList[0]['monthlyAvePcClkCnt'] )
print("월 평균 클릭수_Mobile",keywordList[0]['monthlyAveMobileClkCnt'] )
print("월 평균 클릭률_PC: ",keywordList[0]['monthlyAvePcCtr'] )
print("월 평균 클릭수_Mobile: ",keywordList[0]['monthlyAveMobileCtr'] )
print("경쟁정도: ",keywordList[0]['plAvgDepth'] )
print("월평균 노출 광고수: ",keywordList[0]['compIdx'] )
