#coding=utf-8
from urllib.request import urlopen
from urllib.parse import quote
import string
import json
import requests
from prettyprinter import pprint

print("    I love animals.");
print("              ┏┓      ┏┓");
print("            ┏┛┻━━━┛┻┓");
print("            ┃      ☃      ┃")
print("            ┃  ┳┛  ┗┳  ┃")
print("            ┃      ┻      ┃")
print("            ┗━┓      ┏━┛")
print("                ┃      ┗━━━┓")
print("                ┃  神兽保佑    ┣┓")
print("                ┃ 永无BUG！   ┏┛")
print("                ┗┓┓┏━┳┓┏┛")
print("                  ┃┫┫  ┃┫┫")
print("                  ┗┻┛  ┗┻┛")
print("      ")

def mkdir(path):
    # 引入模块
    import os
 
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
 
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists=os.path.exists(path)
 
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path) 
        print(path+' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False
def upload_file(fileUrl, filePath, fileName):
    try:
        pic = requests.get(fileUrl, timeout=15)
        string = filePath + '/' + str(fileName) + '.jpg'
        with open(string, 'wb') as f:
            f.write(pic.content)
            print('成功下载第%s张图片: %s' % (fileName, str(fileUrl)))
    except Exception as e:
        print('下载第%s张图片时失败: %s' % (fileName, str(fileUrl)))
        print(e)

filePath = "./baiduImages";
mkdir(filePath)
# 设置搜索值
searchName = "小狗";
row = 30;
i = 1;
gsm = "1e"
while i>=0:
    page = row*i;
    num = 1560496791090 + page
    i = i+1;
    url = "https://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord="+searchName+"&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&word="+searchName+"&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&expermode=&force=&pn="+str(page)+"&rn="+str(row)+"&gsm="+gsm
    print(url);
    responese = urlopen(quote(url,safe = string.printable))
    responeseData = responese.read();
    responeseJson = json.loads(responeseData);
    if len(responeseJson['data']) == 0:
        break
    gsm = responeseJson['gsm']
    for j in range(len(responeseJson['data'])):
        if len(responeseJson['data'][j]) == 0:
            continue
        upload_file(responeseJson['data'][j]['hoverURL'], filePath, str(i) + str(j))
