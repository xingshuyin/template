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
import os
import sys
import time
# ps -ef|grep "news"|cut -c 9-16|xargs kill -9   批量关闭进程
# nohup python run.py > news.out 2>&1 &       服务器上的启动命令.同文件目录下执行
sys.path.append(r'/home/wjt/back')  # 将项目路径添加到系统搜寻路径当中
# sys.path.append(r'P:\wjt\back')  # 将项目路径添加到系统搜寻路径当中
os.environ['DJANGO_SETTINGS_MODULE'] = 'root.settings'  # 项目名.settings
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django

django.setup()
import scrapy
from system.models import Spider
from scrapy.crawler import CrawlerRunner
from multiprocessing import Process
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from system.news.news.spiders.common import CommonSpider


def main():
    start = time.time()
    configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    spiders = Spider.objects.filter(enable=True).values()
    for i in list(spiders):
        print('运行- ', i['name'])
        runner.crawl(CommonSpider, rule=i)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished
    end = time.time()
    print('程序运行时间为: %s s' % (end - start))


# def run():
#     p = Process(target=main)
#     p.start()
#     p.join()

if __name__ == '__main__':
    main()
    # schedule.every(6).hours.do(main)  # 每12小时运行一次
    # schedule.every(3).minutes.do(run)  # 每12小时运行一次
    # while True:
    #     schedule.run_pending()
