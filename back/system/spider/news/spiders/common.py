import re
from time import time, sleep
from ..tools import path, deal_path
from ..items import NewsItem
from ..pipelines import NewsPipeline
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import copy
from hashlib import md5

from system.models import Article
from scrapy.http import Request, Response, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Spider

from hashlib import md5
import django
from system.models import Category
import random
import requests
from django.db import close_old_connections, connections
import time

# from scrapy.utils.asyncgen import collect_asyncgen
# from scrapy.utils.spider import iterate_spider_output
default_cover = {
    12: ['http://121.89.199.142/api/media/cover/hot1.jpg', 'http://121.89.199.142/api/media/cover/hot2.png'],
    14: ['http://121.89.199.142/api/media/cover/notice1.jpg', 'http://121.89.199.142/api/media/cover/notice2.png'],
    13: ['http://121.89.199.142/api/media/cover/news1.jpg', 'http://121.89.199.142/api/media/cover/news2.jpg'],
    15: ['http://121.89.199.142/api/media/cover/media1.png', 'http://121.89.199.142/api/media/cover/media2.png'],
    16: ['http://121.89.199.142/api/media/cover/performance1.jpg', 'http://121.89.199.142/api/media/cover/performance2.jpg'],
}


class CommonSpider(CrawlSpider):  # https://docs.scrapy.org/en/latest/topics/spiders.html#crawlspider
    '''通用爬虫'''
    name = "CommonSpider"
    pipline = set([NewsPipeline])

    def __init__(self, rule):
        '''初始化

        Args:
            rule (dict): 爬虫规则
        '''
        for i in connections.all():
            i.close()
        self.count = 0
        self.rule = rule
        self.name = rule['name']
        # self.allowed_domains = rule['allowed_domains'].split(",")
        self.allowed_domains = ['*']
        self.start_urls = rule['start_urls'].split(",")
        rule_list = []
        self.page_seen = set()
        # 分页提取规则
        if rule['xpath_page_restrict']:
            rule_list.append(Rule(LinkExtractor(allow=(rule['re_page'], ), restrict_xpaths=[rule['xpath_page_restrict']])))
        # ../../scgl/.*.html
        # 文章链接提取规则
        rule_list.append(Rule(LinkExtractor(allow=rule['re_item'], restrict_xpaths=[rule['xpath_item_restrict']]), callback='parse_item'))

        self.rules = tuple(rule_list)
        super(CommonSpider, self).__init__()

    def parse_start_url(self, response, **kwargs):
        '''判断是否构造分页链接

        Args:
            response (): 响应

        Returns:
            list: []

        Yields:
            Request: 分页数据请求
        '''
        if self.rule['re_page_num']:
            pages = response.css('*').re(self.rule['re_page_num'])  # 正则匹配页码,最终使用第一个匹配到的页数
            if len(pages) > 0:
                for num in range(int(self.rule['start_page_num']), int(pages[0]) + int(self.rule['start_page_num'])):
                    if self.rule['page_format_shift']:
                        num = eval(self.rule['page_format_shift'])
                    yield scrapy.Request(url=self.rule['page_format'].format(num), method="GET", callback=lambda r: self._requests_to_follow(r), dont_filter=True)
        return []

    def _requests_to_follow(self, response):
        '''匹配所有rule_list里的规则
        '''
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for rule_index, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response) if lnk not in seen]
            for link in rule.process_links(links):
                seen.add(link)
                if rule.link_extractor.restrict_xpaths[0] == self.rule['xpath_page_restrict']:
                    if link.url not in self.page_seen:  #  分页链接去重
                        self.page_seen.add(link.url)
                        yield scrapy.Request(url=link.url, method="GET", callback=lambda r: self._requests_to_follow(r), dont_filter=True)
                    else:
                        pass
                else:
                    # yield scrapy.Request(url=link.url, method="GET", callback=lambda r: self.parse(r), dont_filter=True)

                    if Article.objects.filter(url_hash=md5(link.url.encode(encoding='UTF-8')).hexdigest()).exists():
                        # sleep(1)
                        continue
                    else:
                        print('获取新的文章', link.url)
                        yield scrapy.Request(url=link.url, method="GET", callback=lambda r: self.parse(r), dont_filter=True)

    def parse(self, response):
        '''请求/解析文章详情页
        '''
        createAt = response.xpath(self.rule['xpath_time'])
        if self.rule['re_time']:
            createAt = createAt.re(self.rule['re_time'])
            if len(createAt) > 0:
                createAt = createAt[0].replace('\n', '').strip()
            else:
                createAt = None
        else:
            createAt = ''.join(createAt.getall()).replace('\n', '').strip()
        cover = response.xpath(self.rule['xpath_cover']).re('<img.*?src="(.*?)".*?>')
        if len(cover) > 0:
            cover = path(cover[0], response)
        else:
            cover = None
        # content = ''.join(response.xpath(self.rule['xpath_content']).getall()).replace('\n', '').strip()  # 获取文章内容
        content = response.xpath(self.rule['xpath_content']).getall()[0].replace('\n', '').strip()  # 获取文章内容
        content = deal_path(content, response)  # 处理所有相对路径的链接
        name = ''.join(response.xpath(self.rule['xpath_name']).getall()[:2]).replace('\n', '').strip()  # 获取文章名称
        source = response.xpath(self.rule['xpath_source'])
        if self.rule['re_source']:
            source = source.re(self.rule['re_source'])  # 获取文章来源
            if len(source) > 0:
                source = source[0].replace('\n', '').strip()
            else:
                source = None
        else:
            source = ''.join(source.getall()).replace('\n', '').strip()

        item = NewsItem()
        item['url'] = response.url
        item['category'] = self.rule['category_id']
        item['name'] = name
        item['cover'] = cover
        item['pub_time'] = createAt
        item['content'] = content
        item['source'] = source

        item['category'] = Category.objects.get(id=item['category'])
        item['url_hash'] = md5(item['url'].encode(encoding='UTF-8')).hexdigest()
        item['type'] = 3
        if not item['cover']:
            item['cover'] = random.choice(default_cover[item['category'].id])

        if self.count > 5:
            self.count = 0
        if self.count == 0:
            for i in connections.all():
                i.close()
        self.count += 1

        # if Article.objects.filter(url_hash=item['url_hash']).exists():
        #     # sleep(1)
        #     Article.objects.filter(url_hash=item['url_hash']).update(content=content)
        #     print('更新成功----------', item['url'])
        #     return

        try:
            item.save()

            print('保存成功----------', item['url'])
        except:
            close_old_connections()
            print('保存失败----------', item['url'])

        # return item
