import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.xiaohongshu.com/user/profile/66a1c69d0000000024022d87"   # URL to be checked
headers = {
    'Cookie': 'abRequestId=4de56bb4-0d40-56f6-83b4-64f7fad614c2; a1=190c02cb7720rfrcaeplz9mevooeyoe7rb066ior450000149041; webId=4a643b16f39b307924f577607a974c95; gid=yj8S8JSDiYFYyj8S8JSDWD3lWJ8FiFS0dU1u8F4j6dhllK28dvldWK888y4j84y828fj2dij; customerClientId=782604908622622; x-user-id-partner.xiaohongshu.com=66bf0b81e200000000000001; x-user-id-zhaoshang.xiaohongshu.com=66c8427ee300000000000001; x-user-id-pgy.xiaohongshu.com=66c8427ee300000000000001; x-user-id-ad.xiaohongshu.com=641bfd852e034300017771d2; x-user-id-ad-market.xiaohongshu.com=66bf0b81e200000000000001; access-token-ad-market.xiaohongshu.com=customer.ad_market.AT-68c5174199821849254868919t3b50rde9gnfqbk; access-token-open.xiaohongshu.com=customer.open.AT-68c517420325485956523702hern9hrcfpufhlou; access-token-open.beta.xiaohongshu.com=customer.open.AT-68c517420325485956523702hern9hrcfpufhlou; webBuild=4.36.5; xsecappid=xhs-pc-web; unread={%22ub%22:%2263f0d8cb00000000130316d3%22%2C%22ue%22:%22645a27c9000000001101322a%22%2C%22uc%22:17}; web_session=0400698e4051025616b8701fcf344ba446e5b2; acw_tc=3ff7313d22d2c32c0283c303641bb8aacad65bd048583bc34e98257108f11688; websectiga=634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a; sec_poison_id=90cb33e4-eaee-4241-9511-e22dd59a5d14',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}
response = requests.get(url,headers=headers)   # Sending a GET request to the URL

if response.status_code == 200:   # Checking if the status code of the response is 200 (OK)
    html=BeautifulSoup(response.text,'html.parser')
    count = html.select(".data-info .user-interactions .count")   # Selecting the title tag of the HTML page
    for item in count:
        print(item.text)   # Printing the count of the user interactions
        
    print("The URL is accessible.")
else:
    print("The URL is not accessible.")   # If the status code is not 200, the URL is not accessible.   

# 小红书
driver = webdriver.Chrome()   # Opening the Chrome browser()
driver.get("https://www.douyin.com/user/MS4wLjABAAAAmOY4l8W-lPp4chARlFapKA0RlWhPVonqvv1p787ciV8?from_tab_name=main")
driver.implicitly_wait(10)
elem = driver.find_elements(By.CLASS_NAME, "C1cxu0Vq")
for item in elem:
    print(item.text)
driver.close()