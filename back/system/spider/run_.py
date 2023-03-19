from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.cmdline import execute
import schedule
import time
# nohup python run.py > news.out 2>&1 &


def main():
    setting = get_project_settings()
    process = CrawlerProcess(setting)
    process.crawl('culture_tz')
    process.crawl('culture_whyw')
    process.crawl('culture_hb_zyxx')
    process.crawl('culture_hb_mygz')
    process.crawl('culture_gg')
    process.start()


def run():
    print('爬虫启动')
    execute('scrapy crawl culture_tz'.split())
    execute('scrapy crawl culture_whyw'.split())
    execute('scrapy crawl culture_hb_zyxx'.split())
    execute('scrapy crawl culture_hb_mygz'.split())
    execute('scrapy crawl culture_gg'.split())


if __name__ == '__main__':
    schedule.every().day.at("22:23").do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)
    # run()
