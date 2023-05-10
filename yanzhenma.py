import ddddocr
import os
import base64 
import requests
import urllib

# res = requests.get("http://crm-s1.localhost.com/admin/login/verify.html")
strs = urllib.request.urlopen('http://1.117.245.253/admin/login/verify').read()
# data = strs.decode().strip().split(",")
# strs.replace('data:image/jpeg;base64,','')
 
# print(data[1])
# exit()
# imgdata=base64.b64decode(data[1])
file=open('1.jpg','wb')
file.write(strs)
file.close()
# exit()

ocr = ddddocr.DdddOcr()
with open('1.jpg', 'rb') as f:
    img_bytes = f.read()
res = ocr.classification(img_bytes)
print(res)