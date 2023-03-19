# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql
import re
from openpyxl import Workbook

db = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',  #在这里输入用户名
    password='123456',  #在这里输入密码
    # charset='utf8mb4',
    database='template')  #连接数据库
cursor = db.cursor()


class SpiderPipeline:

    def open_spider(self, spider):
        # self.wb = Workbook() # 保存到excel时需要这三行和close_spider的一行
        # self.ws = self.wb.active
        # self.ws.title = 'MS'
        pass

    def close_spider(self, spider):
        # self.wb.save('data.xlsx') # excel保存位置
        pass

    def process_item(self, item, spider):
        print('process_item')
        item['content'] = item['content'].replace('\'', '')
        item['content'], num = re.subn('<script.*?</script>', '', item['content'])

        # self.ws.append(item.values())  # 保存到excel

        sql = f"""
        INSERT IGNORE INTO `article` (`name`, `source`, `pub_time`, `content`, `type`, `url`, `url_hash`)  VALUES  ('%s', '%s', '%s', '%s', %s,'%s','%s')
        """ % (item['name'], item['source'], item['pub_time'], item['content'], item['type'], item['url'], item['url_hash'])
        r = cursor.execute(sql)
        if r != 0:
            print(item['name'])
        db.commit()
