import http.client
import json
import xlsxwriter as xw
import time
import math

def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("sheet1")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['达人昵称','达人UID','豁免周期']  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for j in range(len(data)):
        a = str(data[j]["add_time_ms"])[:-3]
        startimeArray = time.localtime(int(a))
        star_date = time.strftime("%Y-%m-%d %H:%M:%S", startimeArray)
        b = str(data[j]["expire_time_ms"])[:-3]
        endtimeArray = time.localtime(int(b))
        end_date = time.strftime("%Y-%m-%d %H:%M:%S", endtimeArray)
        insertData = [data[j]["nickname"], data[j]["user_id"], '{}至{}'.format(star_date, end_date)]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1
    workbook.close()  # 关闭表

conn = http.client.HTTPSConnection("buyin.jinritemai.com")
payload = ''
cookie = "is_staff_user=false; store-region-src=uid; qc_tt_tag=0; store-region=cn-sh; passport_csrf_token=59268c5a8d0301582c7abffaebf8b3f8; passport_csrf_token_default=59268c5a8d0301582c7abffaebf8b3f8; s_v_web_id=verify_magdncxt_4NkgkFFE_Zy9O_4eDR_ARqH_TjjmujME4vpu; gfkadpd=2631,22740; _tea_utm_cache_3813=undefined; Hm_lvt_b6520b076191ab4b36812da4c90f7a5e=1749117989,1749608374; HMACCOUNT=CDA2B9AF1C6D1D00; buyin_shop_type=11; buyin_account_child_type=1; buyin_app_id=13; buyin_shop_type_v2=11; buyin_account_child_type_v2=1; buyin_app_id_v2=13; ttwid=1%7C5Jrf6T2LuvpEkiOvGIksJVMlikBPtRnOhnb-7DibTWI%7C1749608421%7C992b46a96bae93c6c71852a26f22fdd0c9de3589f4240f742323a9f31a6de434; passport_mfa_token=CjHgAhTap0pzHn%2BjzaHj%2B4GVS5nJYzAfFwFNvvLAJJpjLHIP2UOewfMDGita%2FhnDy5JAGkoKPAAAAAAAAAAAAABPGWiF%2FMbbtne8kPtwEkj9VBqK1XBHt5MJZ4ub2K0wr8duK%2BLKIZePK6OLLYi%2FCjY3tBCe4%2FMNGPax0WwgAiIBAyzL2Jc%3D; odin_tt=39a0327a45d55998eb665fec3a3736a622593a507419bc2a0f2cf599f9f6e0a159858bc6327f55ed4ff5ad20469f333374d7d163028183664c91d88567b5fcbf; uid_tt=5a8cf1267a70689ef4fc94c95a5d98bd; uid_tt_ss=5a8cf1267a70689ef4fc94c95a5d98bd; sid_tt=9f673cb13dd863c6e43a5ae591245f0a; sessionid=9f673cb13dd863c6e43a5ae591245f0a; sessionid_ss=9f673cb13dd863c6e43a5ae591245f0a; ucas_c0=CkEKBTEuMC4wEKaIhKrs_bmkaBjmJiDAlvCl3oysBSiwITD30MChz_SLBkDzz6PCBkjzg-DEBlClvLOW7PussWBYbhIUos3ug6nFrocYAOfStVYalwQwmwI; ucas_c0_ss=CkEKBTEuMC4wEKaIhKrs_bmkaBjmJiDAlvCl3oysBSiwITD30MChz_SLBkDzz6PCBkjzg-DEBlClvLOW7PussWBYbhIUos3ug6nFrocYAOfStVYalwQwmwI; PHPSESSID=2fa59c3efe0379026603ff3a0651e492; PHPSESSID_SS=2fa59c3efe0379026603ff3a0651e492; Hm_lpvt_b6520b076191ab4b36812da4c90f7a5e=1749608444; sid_guard=9f673cb13dd863c6e43a5ae591245f0a%7C1749608445%7C5184000%7CSun%2C+10-Aug-2025+02%3A20%3A45+GMT; sid_ucp_v1=1.0.0-KDgyMzEzOGMyODJiYTFlZDQwM2JhNGRmYTgwZjY4YTNhZTQ4MGU0OGYKGQj30MChz_SLBhD9z6PCBhiwISAMOAFA6wcaAmxxIiA5ZjY3M2NiMTNkZDg2M2M2ZTQzYTVhZTU5MTI0NWYwYQ; ssid_ucp_v1=1.0.0-KDgyMzEzOGMyODJiYTFlZDQwM2JhNGRmYTgwZjY4YTNhZTQ4MGU0OGYKGQj30MChz_SLBhD9z6PCBhiwISAMOAFA6wcaAmxxIiA5ZjY3M2NiMTNkZDg2M2M2ZTQzYTVhZTU5MTI0NWYwYQ; ucas_c0_buyin=CkEKBTEuMC4wEICIgrCc_7mkaBjmJiDAlvCl3oysBSiwITD30MChz_SLBkD9z6PCBkj9g-DEBlClvLOW7PussWBYbhIURkWu5n0_BPiDGbjpue7Ldxc__Lw; ucas_c0_ss_buyin=CkEKBTEuMC4wEICIgrCc_7mkaBjmJiDAlvCl3oysBSiwITD30MChz_SLBkD9z6PCBkj9g-DEBlClvLOW7PussWBYbhIURkWu5n0_BPiDGbjpue7Ldxc__Lw; COMPASS_LUOPAN_DT=session_7514509181861445940; SASID=SID2_7514510012757049609; BUYIN_SASID=SID2_7514510012757049609; scmVer=1.0.1.8978; csrf_session_id=3d8ae466f14aa2b3af2d8024d7c7cc5d"
headers = {
   'Cookie': cookie,
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Host': 'buyin.jinritemai.com',
   'Connection': 'keep-alive'
}
page = 1
datares = []
total = 126
while page < total:
    conn.request("GET", "/api/commission_invoice/exempt/query?tab=effect&author_info=&size=20&page={}&verifyFp=verify_m06efetn_mNMjZux6_0XI7_4vbA_BwAB_Q2gSc42YhSUS&fp=verify_m06efetn_mNMjZux6_0XI7_4vbA_BwAB_Q2gSc42YhSUS&msToken=puKnGTGjWqZazJcCaoqnkZC679AvjOHhcskoDiMCd05OjCKWZoFJIC6WoZViDfVe2IWDq0FwIVmYvhIGDFNBjzOx8ESiPtOtB-QJfaiHMmPXhkMMBB9sGBe7-zI%3D&a_bogus=D6R0%2FQhhdE2NkfLg5IcLfY3qfbl3YDME0GJXMDgbynvL0y39HMTf9exElWiveSyjN4%2FkIeEjy4hbYrogrQCJ0Zwf7Wsx%2F2CZmyh0t-P2so0j53intL6mE0hN-Jj3SFlm5XNAEOJ0y75bFR70WoOnmhK4bfebY7Y6i6trcD%3D%3D".format(page), payload, headers)
    res = conn.getresponse()
    data = res.read()
    page += 1
    
    res_data = json.loads(data.decode("utf-8"))['data']['author']
    total = math.ceil(json.loads(data.decode("utf-8"))['data']['total']/20) + 1
    if res_data is not None:
        datares += res_data
# print(total)
xw_toExcel(datares, './豁免达人（生效中）.xlsx')
print(len(datares))