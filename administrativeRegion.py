## 获取行政区号及对应的名称
## 来源：https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html
import requests 
import bs4
import pymysql
import json

# 请求处理
async def fetchUrl(url):
	browser = await launch({'headless': False,'dumpio':True, 'autoClose':True})
	page = await browser.newPage()

	await page.goto(url)
	await asyncio.wait([page.waitForNavigation()])
	str = await page.content()
	await browser.close()
	soup = bs4.BeautifulSoup(str, 'html.parser') 
	tr = soup.select(".item-yxmc")
	i = 0;
	while i<len(tr):
		a = tr[i].get_text().strip()
		if a:
			print(a)
		i += 1
j = 0
while j < 3:
	url = "https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html"
	# print(url)
	asyncio.get_event_loop().run_until_complete(fetchUrl(url))
	j += 1
exit()

# 设置数据库参数
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
next_base_url = "https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/"
while j<int(page_num):
	#输出数据量
	print(j*20)    
	res = requests.get(next_base_url) 
	res.raise_for_status() 
	soup = bs4.BeautifulSoup(res.text, 'html.parser') 
	tr = soup.select(".item-container")
	i = 0
	a = ""
	a1 = ""
	#执行新增语句
	sql = """INSERT INTO school(name, level_text) VALUES """ + a
	sql1 = """INSERT INTO major(s_id,name) VALUES """ + a1
	j = j + 1
	try:
	   	# 执行sql语句	
	   	cursor.execute(sql)
	   	# 提交到数据库执行
        db.commit()
	except:
	   	# 如果发生错误则回滚
	   	print(sql)
	   	db.rollback()
# 关闭db连接
db.close()
exit()

 
 
 
