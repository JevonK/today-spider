import requests
import json

myobj = {'pageNum': '1', 'pageSize': 1000, 'productId': 323, 'status': 1}

header = {'token' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxODAzMDMiLCJleHAiOjE2ODUyNjM3MTF9.ii_e2nKsBZssB2o725Jg0yswy3SaJp2prWfFwlT0Ok4', 'tel': '13797160119'}

res = requests.post("https://kuaihuan.art:8083/api/selectResellProduct2", data = myobj, headers = header).json()
# print(len(res['data']['data']))
# exit()
j = 0
for i in res['data']['data']:
    if i['isShowLock'] == 2:
        j += 1
print(j)

# print(requests.post("https://kuaihuan.art:8083/api/selectResellProduct2", data = myobj, headers = header).text)
