import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = "https://www.xiaohongshu.com/user/profile/66a1c69d0000000024022d87"   # URL to be checked
headers = {
    'Cookie': '',
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