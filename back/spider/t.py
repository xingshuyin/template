import pymysql

db = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',  #在这里输入用户名
    password='123456',  #在这里输入密码
    # charset='utf8mb4',
    database='template')  #连接数据库
cursor = db.cursor()
sql = """
       select 1 from  `article` where url_hash = '0364566e762c63e9f7b7107e26261d6fa199' limit 1
"""
cursor.execute(sql)
print(cursor.fetchone())
