import http.client

conn = http.client.HTTPSConnection("www.shutuiche.com")
payload = ''
headers = {
   'Cookie': 'PHPSESSID=gecg6tuiqmukdhotg3t59v7ii8',
   'Token': '',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Accept': '*/*',
   'Host': 'www.shutuiche.com',
   'Connection': 'keep-alive'
}
ids = [1472,1481,1470,1471,1474,1475,1477,1479,1480,1482,1483,1484,1486,1487,1488,1489,1492,1493,1495,1498]
for i in ids:
    conn.request("GET", "/admin/feishu_execute/syncExecuteTable?activity_id="+str(i), payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(i)
    print(data.decode("utf-8"))