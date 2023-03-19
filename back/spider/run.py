'''
Filename     : run.py
Description  : wjt-爬虫-启动文件
Author       : xingshuyin xingshuyin@outlook.com
Date         : 2022-11-03 11:15:17
LastEditors  : xingshuyin xingshuyin@outlook.com
LastEditTime : 2022-11-17 09:32:08
Copyright (c) 2022 by Research Center of Big Data and Social Computing DARG, All Rights Reserved.
'''
from twisted.internet import reactor
import time
import pymysql
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spider.spiders.article import ArticleSpider

rule = [{
    'name': '河北文旅厅-媒体关注',
    'allowed_domains': '*',  # 域名列表(逗号分隔)
    'start_urls': 'http://www.hebeitour.gov.cn/xwzx/mtgz/index.html',  # 开始页(逗号分隔)
    'start_page_num': None,  # 分页页数开头
    'max_page_num': None,  # 分页页数最大值 --- 优先使用分页页数正则而不是最大值
    're_page_num': None,  # 分页页数正则
    'page_format': None,  # 分页链接格式化字符(和分页正则同时存在)
    'page_format_shift': None,  # 分页链接页码转换(传入num判断并修改)(和分页正则同时存在)
    # 上下两块选其一
    'xpath_page_restrict': '//span[contains(text(), "下一页")]/parent::a',  # 分页链接提取区域xpath(必填)
    're_page': '.*/index_.*',  # 分页链接正则(必填)
    'xpath_item_restrict': '//div[@class="list"]/ul/li/a',  # 内容链接提取区域xpath(必填)
    're_item': '.*/c/.*',  # 内容链接正则(必填)
    'xpath_name': '//div[@class="content"]/h1/text()',  # 标题xpath(必填)
    'xpath_time': '//div[@class="post_source"]/text()',  # 时间xpath(必填)
    're_time': '(.*?)来源.*?',  # 时间正则(选填)
    'xpath_cover': '//div[@id="content"]',  # 封面xpath(一般和内容xpath一样就行)
    'xpath_content': '//div[@id="content"]',  # 内容xpath(必填)
    'xpath_source': '//div[@class="post_source"]/text()',  # 来源xpath(必填)
    're_source': '.*?来源：(.*)',  # 来源正则(选填)
    'enable': 1,  # 是否启用
}]


def main():
    start = time.time()
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    cursor.execute('SELECT * FROM `spider`')
    spiders = cursor.fetchall()
    cursor.close()
    db.close()
    for i in spiders:
        print('运行- ', i['name'])
        runner.crawl(ArticleSpider, rule=i)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    end = time.time()
    print('程序运行时间为: %s s' % (end - start))


if __name__ == '__main__':
    db = pymysql.connect(
        host="localhost",
        port=3306,
        user='root',  #在这里输入用户名
        password='123456',  #在这里输入密码
        charset='utf8mb4',
        db='template')  #连接数据库
    cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
    main()
