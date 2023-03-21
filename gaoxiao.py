import requests 
import bs4
import pymysql
import json
from xpinyin import Pinyin
 
host = "localhost"
user = "root"
password = "123456"
database = "test"
# 打开数据库连接
db = pymysql.connect(host, user, password, database)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
#判断是否存在学校表（school）和专业表（major）
cursor.execute("drop table if exists school")
cursor.execute("drop table if exists major") 
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
#第一次打开网页
res = requests.get('https://gaokao.chsi.com.cn/sch/search.do?start=0') 
 
res.raise_for_status() 
soup = bs4.BeautifulSoup(res.text, 'html.parser') 
#获取总页数
page_num = soup.select('.ch-page li')[7].string
th = soup.select('th')
th_herd = []
#申明汉子转换拼音对象
pin = Pinyin() 
field = ""
for item in th:
	field += (","+pin.get_pinyin(item.get_text(), '_')+" varchar(100)")
	th_herd.append(pin.get_pinyin(item.get_text(), '_'))
#学校表创建sql语句
sql = """CREATE TABLE school (id int NOT NULL AUTO_INCREMENT """+field+""",PRIMARY KEY ( id ))"""
sql1 = """CREATE TABLE major (s_id int , name varchar(100))"""
#执行语句
cursor.execute(sql);
cursor.execute(sql1);
# 转化数组为逗号分隔的字符串
delimiter = ','
field = delimiter.join(th_herd)
j = 0
m = 1
while j<int(page_num):
	#输出数据量
	print(j*20) 
	res = requests.get('https://gaokao.chsi.com.cn/sch/search.do?start=%s'%(j*20)) 
	res.raise_for_status() 
	soup = bs4.BeautifulSoup(res.text, 'html.parser') 
	tr = soup.select("table tr")
	i = 0
	a = ""
	a1 = ""
	while i<len(tr):
		if i == 0:
			i += 1
			continue
		b = ''
		for x in tr[i].select('td')[5].select('span'):
			b = b + "    " + str(x.get_text())
		c = (1 if (tr[i].select('td')[6].string) is None else 0)
		d = (";" if (i+1) is len(tr) else ",")
		a += "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')%s" % (tr[i].select('td')[0].get_text().strip(), tr[i].select('td')[1].get_text().strip(), tr[i].select('td')[2].get_text().strip(),tr[i].select('td')[3].get_text().strip(), tr[i].select('td')[4].get_text().strip(), b, c, tr[i].select('td')[7].get_text().strip(), d)
		#获取学校专业
		##查询学校
		res1 = requests.get('https://gaokao.chsi.com.cn/zyk/pub/myd/specAppraisalTop.action?yxmc=%s'%(tr[i].select('td')[0].get_text().strip())) 
		res1.raise_for_status() 
		soup1 = bs4.BeautifulSoup(res1.text, 'html.parser') 
		url = soup1.select('.check_detail')
		##查看全部专业
		u = 0
		for x in url:
			if u > 1:
				break
			u = u + 1
			res1 = requests.get('https://gaokao.chsi.com.cn/%s'%(x['href'])) 
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
	sql = """INSERT INTO school("""+field+""") VALUES """ + a
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
 
 
 