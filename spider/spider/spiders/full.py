from hashlib import md5
import re
import scrapy
import json
import os
import time
from ..tools import path, deal_path, script_shot, script
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy_splash.response import SplashTextResponse
from fake_useragent import UserAgent



job_rule = {
    'name': 'job.hebust',
    'start_urls': 'https://job.hebust.edu.cn/teachin',  # 开始页(逗号分隔)
    'allowed_domains': 'hebust.edu.cn',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="single-content"]//img/@src', # 有了get_img就是纯图片抓取 contentrule无效
    'contentrule': {
        # 'img': {'xpath':'//div[@class="single-content"]//img/@src', 're': ''}, # 获取文章的图片链接
        '标题': {'xpath': '//div[@class="title-message"]//h5/text()', 're': ""},
        '文章源码': {'xpath': '//div[@class="info"]//text()', 're': ""},
        '文章内容': {'xpath': '//div[@class="info"]//*[name()!="script" and name()!="style"]/text()', 're': ""}, # 去掉scrpit/style标签
    },
    're_page': '.*?teachin/index.*',  # 分页链接正则(必填)
    're_item': '.*?teachin/view/id/\d+',  # 内容链接正则(必填)
}
args = {'wait': 2, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}

output = r"/mnt/d/python/template/spider"
ua = UserAgent()
req = 'playwright'
def get_all(response, xpath):
    try:
        return ''.join(response.xpath(xpath).getall())
    except:
        return None


class FullSpider(CrawlSpider):
    name = "full"
    seen = set()
    custom_settings = {
        'CONCURRENT_REQUESTS': 5,
        'DOWNLOAD_DELAY': 0
    }

    def __init__(self):
        self.rule = job_rule
        self.allowed_domains = self.rule.get('allowed_domains', '*')
        self.name = self.rule['name']
        self.start_urls = self.rule['start_urls'].split(",")
        self.rules = [
            Rule(LinkExtractor(allow=self.rule['re_item'], restrict_xpaths=[self.rule['get_item']]),
                 callback='parse_item', process_request='process_item', follow=True),
            Rule(LinkExtractor(allow=self.rule['re_page'], restrict_xpaths=[self.rule['get_page']]),
                 callback='_requests_to_follow', process_request='process_page', follow=True)
        ]
        self.image_data = []
        self.article_data = []
        self.start = 0
        super().__init__()

    def start_requests(self):
        print('start_urls', self.start_urls)
        for url in self.start_urls:
            if req =='splash':
                yield SplashRequest(url,
                                    endpoint='execute',
                                    args=args,
                                    dont_filter=True)
            elif req== 'playwright':
                yield scrapy.Request(url, headers={"User-agent": ua.random}, meta={"playwright": True}, dont_filter=True)
            else:
                yield scrapy.Request(url, headers={"User-agent": ua.random}, dont_filter=True)
                
    def process_page(self, request, response):
        # request.priority = 1  # 设置请求权重
        return request

    def process_item(self, request, response):
        # print(response.text)
        # request.priority = 1
        return request

    def _requests_to_follow(self, response):
        # print(response.text)
        # if not isinstance(response, SplashTextResponse):
        #     return

        for rule_index, rule in enumerate(self._rules):
            links = [
                lnk
                for lnk in rule.link_extractor.extract_links(response)
                if lnk not in self.seen
            ]
            if rule_index == 1:
                time.sleep(1)
            for link in rule.process_links(links):
                self.seen.add(link)
                request = self._build_request(rule_index, link)
                yield rule.process_request(request, response)

    def _build_request(self, rule_index, link):
        print(link.url)
        if req =='splash':
            return SplashRequest(
                url=link.url,
                callback=self._callback,
                errback=self._errback,
                meta=dict(rule=rule_index, link_text=link.text),
                endpoint='execute',
                args=args,
                dont_filter=True)
        elif req== 'playwright':
            return scrapy.Request(link.url, headers={"User-agent": ua.random}, callback=self._callback, errback=self._errback, meta=dict(rule=rule_index, link_text=link.text, playwright=True), dont_filter=True)
        else:
            return scrapy.Request(link.url, headers={"User-agent": ua.random}, callback=self._callback, errback=self._errback, meta=dict(rule=rule_index, link_text=link.text), dont_filter=True)
    def parse_item(self, response):
        if 'get_img' in self.rule.keys():
            imgs = response.xpath(self.rule['get_img']).getall()
            print('item ', response.url, len(imgs))
            self.image_data.extend(imgs)
            if time.time() - self.start > 60 * 5:
                self.start = time.time()
                print('共有', len(self.image_data), '个')
                with open(os.path.join(output, f'{self.rule["name"]}.json'), 'w') as f:
                    f.write(json.dumps(self.image_data))
        elif 'contentrule' in self.rule.keys():
            article = {}
            for k, v in self.rule['contentrule'].items():
                if k == 'img':
                    article[k] = response.xpath(v['xpath']).getall()
                else:
                    article[k] = get_all(response, v['xpath'])
                    if v['re']:
                        article[k] = re.search(v['re'], article[k]).groups()
            print('article', article['标题'])

            self.article_data.append(article)

    @staticmethod
    def close(spider, reason):
        with open(os.path.join(output, f'{spider.rule["name"]}_article.json'), 'w') as f:
            f.write(json.dumps(spider.article_data))
            print('共有', '文章', len(spider.article_data), '个')
        with open(os.path.join(output, f'{spider.rule["name"]}_img.json'), 'w') as f:
            f.write(json.dumps(spider.image_data))
            print('共有', '图片', len(spider.image_data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)
