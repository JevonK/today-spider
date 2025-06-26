import http.client
import json
import xlsxwriter as xw
import time
import math
import smtplib
import pymupdf
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from urllib.parse import quote
import threading
import requests
import re
import pandas as pd
from easyofd.ofd import OFD
import base64
from PIL import Image
import numpy as np
import zipfile

# 生成excel文件
def xw_toExcel(data, fileName):  # xlsxwriter库储存数据到excel
    workbook = xw.Workbook(fileName)  # 创建工作簿
    worksheet1 = workbook.add_worksheet("开票详情")  # 创建子表
    worksheet1.activate()  # 激活表
    title = ['开票账单id','开票企业方','订单id',"商品id","账单日期","结算时间","开票金额","结算金额","开票状态"]  # 设置表头
    worksheet1.write_row('A1', title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for item in data[0]:
        insertData = [item["BillId"], item["OutCompanyName"], item["order_id"],item["business_id"],item["statement_date"],item["settle_time"],item["amount_a"],item["amount"],item["status"]]
        row = 'A' + str(i)
        worksheet1.write_row(row, insertData)
        i += 1

    # 设置审核信息
    review_title = ["开票账单id","发票账单id","开票方企业","待开票金额","应开票金额","账单日期","审核通过时间", "审核提交时间", "发票税率", "发票种类", "发票类型", "备注"] # 审核发票信息
    worksheet2 = workbook.add_worksheet("审核信息")  # 创建子表
    worksheet2.activate()  # 激活表
    worksheet2.write_row('A1', review_title)  # 从A1单元格开始写入表头
    cell_format = workbook.add_format()
    cell_format.set_text_wrap()
    image_width = 750.0
    image_height = 480.0
    cell_width = 64.0
    cell_height = 40.0
    x_scale = (cell_width-5) * 1.0 / image_width
    y_scale = (cell_height + 10) * 1.0 / image_height
    worksheet2.set_default_row(cell_height)
    i = 2  # 从第二行开始写入数据
    for item in data[1]:
        insertData = [item["BillId"],item["BillIds"],item["OutCompanyName"],item["Amount"], item["Amounts"],item["AccountDate"],item["ReviewTime"], item["CommitTime"],item["TaxRate"],item["InvoiceKind"],item["InvoiceType"],item["Remark"]]
        row = 'A' + str(i)
        worksheet2.write_row(row, insertData)
        worksheet2.set_row((i - 1), 60)  # 设置图片宽度
        img_inx = 12
        for x in item["ImgPath"]:
            if is_chinese(x) is True:
                worksheet2.write((i - 1), img_inx, x, cell_format)
            else:
                # worksheet2.embed_image((i - 1), img_inx, x)
                worksheet2.insert_image((i - 1), img_inx, x, {'x_offset': 2, 'y_offset': 2, 'x_scale': x_scale, 'y_scale': y_scale, 'positioning': 1})
            img_inx += 1
        i += 1

    # 设置抵扣信息
    payment_title = ["开票账单id","达人付款抵扣金额", "机构付款抵扣金额", "付款抵扣方式","付款抵扣时间","操作单号","失败原因","账单个数","账单总金额","账单类型","发票抬头","收票方税号", "企业名称","企业税号"] # 审核发票信息
    worksheet3 = workbook.add_worksheet("抵扣信息")  # 创建子表
    worksheet3.activate()  # 激活表
    worksheet3.write_row('A1', payment_title)  # 从A1单元格开始写入表头
    i = 2  # 从第二行开始写入数据
    for item in data[2]:
        insertData = [item["BillId"], item["PayAmount"], item["InstitutionPayAmount"],item["PayType"], item["UpdateTime"], item["PayCode"],item["Comment"],item["PayNum"], item["Amount"], item["Scene"],item["IncomeTitle"], item["IncomeCreditCode"], item["OutInvoiceTitle"], item["OutInvoiceCreditCode"]]
        row = 'A' + str(i)
        worksheet3.write_row(row, insertData)
        i += 1


    workbook.close()  # 关闭表

    # 发送邮件
    send_email(fileName)

# 发送邮件
def send_email(filename):
    sender = 'info@seedigitalgroup.com'
    sender_pwd = 'c8aqKdhCRKBNqKdS'
    receivers = ['mengxianlin@seedigitalgroup.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("佣金发票审核", 'utf-8')
    message['To'] =  Header("佣金发票审核", 'utf-8')
    subject = 'OOO-抖店-佣金发票审核'
    message['Subject'] = Header(subject, 'utf-8')

    #邮件正文内容
    message.attach(MIMEText('OOO 抖店-发票管理-佣金发票审核-发票记录一级和二级数据。', 'plain', 'utf-8'))

    # 构造附件1，传送当前目录下的 test.txt 文件
    att1 = MIMEText(open(filename, 'rb').read(), 'base64', 'utf-8')
    att1["Content-Type"] = 'application/octet-stream'
    # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
    att1["Content-Disposition"] = 'attachment; filename="data.xlsx"'
    message.attach(att1)

    try:
        # smtpObj = smtplib.SMTP_SSL("smtp.feishu.cn", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        # smtpObj.login(sender, sender_pwd)
        # smtpObj.sendmail(sender, receivers, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

# pdf 转换为图片
def pyMuPDF_fitz(pdfPath, imagePath, img_name):

    if not os.path.exists(imagePath):#判断存放图片的文件夹是否存在
        os.makedirs(imagePath) # 若图片文件夹不存在就创建

    pdfDoc = pymupdf.open(pdfPath)
    for page in pdfDoc:  # iterate through the pages
        zoom_x = 2.0  # horizontal zoom
        zoom_y = 2.0  # vertical zoom
        mat = pymupdf.Matrix(zoom_x, zoom_y)  # zoom factor 2 in each dimension
        pix = page.get_pixmap(matrix=mat)  # render page to an image
        pix.save(f"{imagePath}/{img_name}.png")  # store image as a PNG


def is_chinese(text):
    """
    检查整个字符串是否包含中文
    :param text: 需要检查的字符串
    :return: bool
    """
    pattern = re.compile(r'[\u4e00-\u9fff]')
    return bool(pattern.search(text))

def ofd_to_images(ofd_path, images_path, filename):
    print(filename)
    with open(ofd_path,"rb") as f:
        ofdb64 = str(base64.b64encode(f.read()),"utf-8")
        ofd = OFD() # 初始化OFD 工具类
        ofd.read(ofdb64,save_xml=False, xml_name="testxml") # 读取ofdb64
        # print(ofd.data) # ofd.data 为程序解析结果
        img_np = ofd.to_jpg() # 转图片

        for idx, img in enumerate(img_np):
            im = Image.fromarray(np.uint8(img))
            im.save(f'%s.png' % (images_path + "/" + filename, ))

# 读取老的execl 表格数据
def get_old_execl(execl_name, sheet_name):
    data_frame=pd.read_excel(execl_name,sheet_name=sheet_name)
    return data_frame

conn = http.client.HTTPSConnection("invoice.bytedance.com")
payload = ''
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo4MTk0OTg2LCJ1c2VyX25hbWUiOiJPVVQtT0YtT0ZGSUNF5a6Y5pa55peX6Iiw5bqXIiwidXNlcl9hdmF0YXIiOiIiLCJ0ZW5hbnRfY29kZSI6InNob3Bfc2Fhc19iYWNrZW5kIiwiZXhwaXJlc19hdCI6MTc1MTAwOTU4NCwiZXh0cmEiOnsiaW5jb21lX3RlbmFudF9jb2RlIjoiYnV5aW5fdG9fZG91ZGlhbiIsInNob3BfaWQiOiI4MTk0OTg2In0sInVzZXJfaWRfc3RyIjoiIiwicm9sZSI6Im1lcmNoYW50In0.ShQCyLdEmy7bFGo9ngPybCdO_AEy-JBh-mEDLf1uQgQ"
headers = {
   'header-invoice-saas-token': token
}
page = 1
execl_data = [] # 发票信息数据
review_data = [] # 发票审核信息数据
payment_data = [] # 发票抵扣信息数据
new_execl_data = [] # 新增发票信息数据
new_review_data = [] # 新增发票审核信息数据
new_payment_data = [] # 新增发票抵扣信息数据
BillDateBegin = "2025-01-01"
BillDateEnd = "2025-06-26"
# BillDateBegin = ""
# BillDateEnd = ""
page_size = 4000
index = 1

execl_path = "./OUT-OF-OFFICE官方旗舰店-佣金发票(2025-01-01~2025-06-26).xlsx"
new_execl_path = "./OUT-OF-OFFICE官方旗舰店-佣金发票(2025-01-01~2025-06-26-new).xlsx"
# execl_path = "./OUT-OF-OFFICE美妆专卖店-佣金发票(all).xlsx"
# new_execl_path = "./OUT-OF-OFFICE美妆专卖店-佣金发票(all-new).xlsx"
# execl_path = "./OUT-OF-OFFICE官方旗舰店-佣金发票(2025-03-01~2025-04-30).xlsx"
# new_execl_path = "./OUT-OF-OFFICE官方旗舰店-佣金发票(2025-03-01~2025-04-30-new).xlsx"

# 判断是否存在历史文件
if os.path.isfile(execl_path):
    old_data = get_old_execl(execl_path, '开票详情')
    order_ids = list(set(old_data["订单id"]))
    old_data = get_old_execl(execl_path, '审核信息')
    auditing_ids = list(set(old_data["开票账单id"]))
    old_data = get_old_execl(execl_path, '抵扣信息')
    deduction_ids = list(set(old_data["开票账单id"]))
else:
    order_ids = []
    auditing_ids = []
    deduction_ids = []

ori_cursor_page = 1
ori_total_page = 1
while ori_cursor_page <= ori_total_page:
    conn.request("GET", f"/biz/api/income/record/reviewedlist?Status=&BillDateBegin={BillDateBegin}&BillDateEnd={BillDateEnd}&PageNo={ori_cursor_page}&PageSize={page_size}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    res_data = json.loads(data.decode("utf-8"))

    # 计算分页数据
    ori_total_page = math.ceil(res_data['Total']/page_size)
    ori_cursor_page += 1

    for item in res_data['RetData']:
        print(index)
        index += 1
        # if item['BillId'] != "202501310000004061":
        #     continue
        # if index > 200:
        #     break
        cursor_page = 1
        total_page = 1
        bill_id = item['BillId']
        amount = item['Amount']
        status = item['Status']
        start_time = int(time.mktime(time.strptime(item['BillDateBegin'], '%Y-%m-%dT%H:%M:%S+08:00')))
        end_time = int(time.mktime(time.strptime(item['BillDateEnd'], '%Y-%m-%dT%H:%M:%S+08:00'))) + 86399
        start_date = time.strftime('%Y-%m-%d', time.localtime(start_time))
        end_date = time.strftime('%Y-%m-%d', time.localtime(end_time))
        out_company_name = item['OutCompanyName']
        cursor = ""
        backwards = True
        new_order_ids_arr = []
        while cursor_page <= total_page:
            conn.request("GET", f"/biz/api/bill/detail/cursor?page_index={cursor_page}&page_size={page_size}&bill_id={bill_id}&scene=DAREN_COMMISSION&start_time={start_time}&end_time={end_time}&backwards={backwards}&cursor={cursor}", payload, headers)
            res_cursor = conn.getresponse()
            data_read = res_cursor.read()
            resp_data = json.loads(data_read.decode("utf-8"))
            # print(len(resp_data['data']))
            is_new_order = False

            for val in resp_data['data']:
                cursor = val['cursor']
                is_new = False

                # 判断订单是否存在
                if not int(val['order_id']) in order_ids:
                    is_new = True
                    is_new_order = True

                obj = {
                    "BillId": bill_id,
                    "OutCompanyName": item['OutCompanyName'],
                    "order_id": val['order_id'],
                    "business_id": val['business_id'],
                    "statement_date": f"{start_date}-{end_date}",
                    "settle_time": val['settle_time'],
                    "amount_a": int(amount)/100,
                    "amount": val['amount']/100,
                    "status": status,
                }

                execl_data.append(obj)
                if is_new is True:
                    new_execl_data.append(obj)

            # 计算分页数据
            total_page = math.ceil(resp_data['total']/page_size)
            cursor_page += 1

        ### 获取发票审核通过信息
        if item['Status'] == "INVOICED":
            conn.request("GET", "/biz/api/income/record/reviewdetail?BatchNo={}".format(item['BatchNo']), payload, headers)
            res_review = conn.getresponse()
            data_read = res_review.read()
            resp_data = json.loads(data_read.decode("utf-8"))
            res_review_data = resp_data['RetData']
            if resp_data['RetCode'] == "0000" and len(res_review_data['InvoiceRecordList']) > 0:
                invoiceRecordList = res_review_data['InvoiceRecordList']
                obj = {
                    "BillId": bill_id,
                    "BillIds": invoiceRecordList[0]['BillIds'],
                    "OutCompanyName": out_company_name,
                    "ReviewTime" : invoiceRecordList[0]['ReviewTime'],
                    "CommitTime" : invoiceRecordList[0]['CommitTime'],
                    "TaxRate" : f"{invoiceRecordList[0]['TaxRate']}%",
                    "InvoiceKind" : invoiceRecordList[0]['InvoiceKind'],
                    "InvoiceType" : invoiceRecordList[0]['InvoiceType'],
                    "AccountDate" : start_date + ' ~ ' + end_date,
                    "Amount" : int(amount)/100,
                    "Amounts" : int(invoiceRecordList[0]['Amount'])/100,
                    "Remark" : invoiceRecordList[0]['Remark'],
                    "ImgPath" : []
                }

                # 下载发票图片
                EInvoiceDetails = json.loads(invoiceRecordList[0]['EInvoiceDetails'])
                for e_invoice_detail in EInvoiceDetails:
                    FileName = e_invoice_detail['Name']
                    TosPath = e_invoice_detail['TosPath']
                    ImgPath = f"D:/temp/images/{TosPath}.png"
                    obj["ImgPath"].append(ImgPath)
                    # 判断文件是否存在
                    if os.path.isfile(ImgPath):
                        continue

                    print(f"正在下载发票图片{bill_id}")
                    OutInvoicerId = res_review_data['InvoiceRelation']['InvoicerId']
                    if is_chinese(FileName):
                        FileName = quote(FileName)
                    img_url = f"https://invoice.bytedance.com/biz/api/income/file/download?FileName={FileName}&TosPath={TosPath}&OutInvoicerId={OutInvoicerId}&OpSource=INCOME"
                    res = requests.get(img_url, headers=headers)
                    data = res.content
                    filetype = FileName[-4:]
                    with open("demo" + filetype, "wb") as code:
                            code.write(data)
                    try:
                        if filetype == '.zip':
                            obj["ImgPath"] = [f"下载地址：{img_url}"]
                        elif filetype == ".ofd":
                            ofd_to_images("demo" + filetype, "images", TosPath)
                        else:
                            pyMuPDF_fitz("demo" + filetype, "images", TosPath)
                            os.remove("demo" + filetype)
                            pass
                    except:
                        obj["ImgPath"].append("不支持下载，请直接上佣金平台下载")
                    # 下载停顿1秒，太密集会无法下载
                    time.sleep(1)

                # obj["ImgPath"] = ""
                review_data.append(obj)
                if not int(bill_id) in auditing_ids:
                    new_review_data.append(obj)

        ### 获取付款抵扣信息
        if item['Status'] == "PAID" or item['Status'] == "UNINVOICED":
            conn.request("GET", "https://invoice.bytedance.com/biz/api/income/record/paydetail?PayCode={}".format(item['PayCode']), payload, headers)
            res_payment = conn.getresponse()
            data_read = res_payment.read()
            resp_data = json.loads(data_read.decode("utf-8"))
            res_payment_data = resp_data['RetData']
            if resp_data['RetCode'] == "0000":
                obj = {
                    "BillId": bill_id,
                    "PayAmount" : int(res_payment_data['PaymentDetail']['PayAmount'])/100,
                    "InstitutionPayAmount" : int(res_payment_data['PaymentDetail']['InstitutionPayAmount'])/100,
                    "PayType" : res_payment_data['PaymentDetail']['PayType'],
                    "UpdateTime" : res_payment_data['PaymentDetail']['UpdateTime'],
                    "PayCode" : res_payment_data['PaymentDetail']['PayCode'],
                    "Comment" : res_payment_data['PaymentDetail']['Comment'],
                    "PayNum" : 1,
                    "Amount" : int(res_payment_data['BillInfo']['Amount'])/100,
                    "Scene" : res_payment_data['BillInfo']['Scene'],
                    "IncomeTitle" : res_payment_data['BillInfo']['IncomeTitle'],
                    "IncomeCreditCode" : res_payment_data['BillInfo']['IncomeCreditCode'],
                    "OutInvoiceTitle" : res_payment_data['BillInfo']['OutInvoiceTitle'],
                    "OutInvoiceCreditCode" : res_payment_data['BillInfo']['OutInvoiceCreditCode'],
                }
                payment_data.append(obj)
                if not int(bill_id) in deduction_ids:
                    new_payment_data.append(obj)
    pass



# print(execl_data)
xw_toExcel([execl_data, review_data, payment_data], execl_path)
xw_toExcel([new_execl_data, new_review_data, new_payment_data], new_execl_path)
print(len(execl_data), len(review_data), len(payment_data))