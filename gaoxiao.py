import requests 
import bs4
import pymysql
import json
from xpinyin import Pinyin
import asyncio
from pyppeteer import launch
 
url = "https://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action?pageCode=10&start=0"
async def fetchUrl(url):
	browser = await launch({'headless': False,'dumpio':True, 'autoClose':True})
	page = await browser.newPage()

	await page.goto(url)
	await asyncio.wait([page.waitForNavigation()])
	str = await page.content()
	await browser.close()
	print(str)
asyncio.get_event_loop().run_until_complete(fetchUrl(url))
exit()

host = "localhost"
user = "root"
passwd = "123456"
db = "test"
# 打开数据库连接
db = pymysql.connect(host=host, user=user, passwd=passwd, db=db)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
#判断是否存在学校表（school）和专业表（major）
cursor.execute("drop table if exists school")
cursor.execute("drop table if exists major") 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
 
#总页数
page_num = 131
th_herd = []
#学校表创建sql语句
sql = """CREATE TABLE school (id int NOT NULL AUTO_INCREMENT, name varchar(100), level_text varchar(100) ,PRIMARY KEY ( id ))"""
sql1 = """CREATE TABLE major (s_id int , name varchar(100))"""
#执行语句
cursor.execute(sql);
cursor.execute(sql1);
j = 0
m = 1
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",}
# 设置cookies
cookies = {}
cookies['goaYXsyEWlxdP'] = '5RryNJKA8FsVqqqDom7.efa1zsJiSqutjquRy41g3IOfmnQMJ1qMbD4qyxORFpryvXo.rDirUKMJXdQdqz.aA6b9f9yucW_q1zNl4Fnks1Wc9BxwulrpILdND5QC3YZlF17F8AK1CBlFFMeDuVeGSL8EEBjuKCCU1.IX9cF3YW5Re3iHTzCFXp4TAUi45sGPGg9YpQlIfk3ZGilJAXdgdo5b7vptiweg4sCPL79Vt9eXniqcl1EnrWNupE4m4AHPkeDga0ZyeawYyWWcCaYcv1i'
cookies['_gat_gtag_UA_100524_6'] = '1'
cookies['_gid'] = 'GA1.3.1516306352.1679714615'
cookies['_ga'] = 'GA1.3.1647652790.1679714615'
cookies['_ga_5FHT145N0D'] = 'GS1.1.1679714614.1.0.1679714614.0.0.0'
cookies['CHSICC01'] = '!GUl2aSGiBZqHIBvzYxYLahOzddj6YxhwgeUGqaJFWcRWQC/piFJ6jSU3QbTab9VQRksllC+CZgaQBQ=='
cookies['35067579362dd9cd78'] = 'c58ea6476bd9c117ebaa07bb7def3eea'
cookies['CHSICC_CLIENTFLAGCHSI'] = '49c3174718c3b560a1040e55b347631e'
cookies['CHSICC_CLIENTFLAGSPECIALITY'] = '93071bb9fa0a5fe0614a9d2141ddeffe'
cookies['goaYXsyEWlxdO'] = '591gVF6cDgwdhC5Uc_6ScHyVOVhYjsD_DCEFzZurz8ua8WhpAdunWd2BT5dZMBBVwElsvrIeo8ow59uGb1UsmCG'
while j<int(page_num):
	#输出数据量
	print(j*20) 
	res = requests.get('https://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action?pageCode=10&start=%s'%(j*20),cookies=cookies, headers=headers, timeout=5) 
	res.raise_for_status() 
	soup = bs4.BeautifulSoup(res.text, 'html.parser') 
	tr = soup.select(".item-container")
	i = 0
	a = ""
	a1 = ""
	while i<len(tr):
		if i == 0:
			i += 1
			continue
		d = (";" if (i+1) is len(tr) else ",")
		a += "('%s', '%s')%s" % (tr[i].select('.item-yxmc').get_text().strip(), tr[i].select('td')[1].get_text().strip(), d)
		#获取学校专业
		##查询学校
		res1 = requests.get('https://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action?yxmc=%s'%(tr[i].select('td')[0].get_text().strip())) 
		res1.raise_for_status() 
		soup1 = bs4.BeautifulSoup(res1.text, 'html.parser') 
		url = soup1.select('.more-text')
		##查看全部专业
		u = 0
		for x in url:
			if u > 1:
				break
			u = u + 1
			res1 = requests.get('https://gaokao.chsi.com.cn%s'%(x['href'])) 
			res1.raise_for_status() 
			soup1 = bs4.BeautifulSoup(res1.text, 'html.parser') 
			td = soup1.select(".first_td")
			j1 = 0
			while j1<len(td):
				if j1 == 0:
					j1 = j1 + 1
					continue
				d1 = ','
				a1 = a1 + "(%s, '%s')%s" % (m, td[j1].get_text().strip(), d1)
				j1 = j1 + 1
		i = i + 1
		m = m + 1
	#执行新增语句
	sql = """INSERT INTO school(name, level_text) VALUES """ + a
	sql1 = """INSERT INTO major(s_id,name) VALUES """ + a1
	j = j + 1
	try:
	   	# 执行sql语句	
	   	cursor.execute(sql)
	   	cursor.execute(sql1[:-1])
	   	# 提交到数据库执行
	   	db.commit()
	except:
	   	# 如果发生错误则回滚
	   	print(sql1)
	   	exit()
	   	db.rollback()
db.close()
 
 
 