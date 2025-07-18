import xlrd

# 打开刚才我们写入的 test_w.xls 文件
wb = xlrd.open_workbook("C:/Users/24282/Downloads/tableConvert.com_9guqx0.xlsx")
# 获取并打印 sheet 数量
print( "sheet 数量:", wb.nsheets)
# 获取并打印 sheet 名称
print( "sheet 名称:", wb.sheet_names())
# 根据 sheet 索引获取内容
sh1 = wb.sheet_by_index(0)
# 也可根据 sheet 名称获取内容
# sh = wb.sheet_by_name('成绩')
# 获取并打印该 sheet 行数和列数
create_sql = "CREATE TABLE IF NOT EXISTS `juguang_report_offline_note` (\n" 
for i in range(sh1.nrows):
    comment_text = sh1.cell_value(i, 0) + "-" + sh1.cell_value(i, 3) + "-" + sh1.cell_value(i, 4)
    field_name = sh1.cell_value(i, 1)
    if sh1.cell_value(i, 2) == "string":
        create_sql += f"`{field_name}` text DEFAULT NULL COMMENT '{comment_text}',\n"

create_sql = create_sql[:-2]

create_sql += "\n) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='笔记层级离线报表数据';"

print(create_sql)

# print( u"sheet %s 共 %d 行 %d 列" % (sh1.name, sh1.nrows, sh1.ncols))
# # 获取并打印某个单元格的值
# print( "第一行第二列的值为:", sh1.cell_value(0, 1))
# # 获取整行或整列的值
# rows = sh1.row_values(0) # 获取第一行内容
# cols = sh1.col_values(1) # 获取第二列内容
# # 打印获取的行列值
# print( "第一行的值为:", rows)
# print( "第二列的值为:", cols)
# # 获取单元格内容的数据类型
# print( "第二行第一列的值类型为:", sh1.cell(1, 0).ctype)