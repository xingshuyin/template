from hashlib import md5
import scrapy
import json
import os
import time
from ..tools import path, deal_path, script_shot, script
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from scrapy_splash.response import SplashTextResponse

image_rule = {
    'name': 'taotuhome_dietutu',
    'start_urls': 'https://taotuhome.com',  # 开始页(逗号分隔)
    'allowed_domains': 'taotuhome.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="single-content"]//img/@src',
    're_page': 'https://taotuhome.com/category/.*?',  # 分页链接正则(必填)
    're_item': 'https://taotuhome.com/\d+.html.*',  # 内容链接正则(必填)
}
article_rule = {
    'name': 'taotuhome_dietutu',
    'start_urls': 'https://taotuhome.com',  # 开始页(逗号分隔)
    'allowed_domains': 'taotuhome.com',
    'get_page': '//body',  # 分页链接提取区域xpath(必填)
    'get_item': '//body',  # 内容链接提取区域xpath(必填)
    'get_img': '//div[@class="single-content"]//img/@src',
    'get_title': '//div[@class="single-content"]//img/@src',
    'get_content': '//div[@class="single-content"]//img/@src',
    'get_author': '//div[@class="single-content"]//img/@src',
    'get_time': '//div[@class="single-content"]//img/@src',
    're_page': 'https://taotuhome.com/category/.*?',  # 分页链接正则(必填)
    're_item': 'https://taotuhome.com/\d+.html.*',  # 内容链接正则(必填)
}
args = {'wait': 2, 'lua_source': script}
args_shot = {'wait': 0.5, 'lua_source': script_shot}


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
        self.rule = image_rule
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
            yield SplashRequest(url,
                                endpoint='execute',
                                args=args,
                                dont_filter=True)

    def process_page(self, request, response):
        request.priority = 10  # 设置请求权重
        return request

    def process_item(self, request, response):
        request.priority = 1
        return request

    def _requests_to_follow(self, response):
        if not isinstance(response, SplashTextResponse):
            return

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
        return SplashRequest(
            url=link.url,
            callback=self._callback,
            errback=self._errback,
            meta=dict(rule=rule_index, link_text=link.text),
            endpoint='execute',
            args=args,
            dont_filter=True)

    def parse_item(self, response):
        # imgs = response.xpath('//div[@class="album"]//div[@class="img-holder"]//img/@src').getall()

        if self.rule['get_content']:
            article = {}
            article['title'] = get_all(response, self.rule['get_title'])
            article['content'] = get_all(response, self.rule['get_content'])
            article['author'] = get_all(response, self.rule['get_author'])
            article['pubtime'] = get_all(response, self.rule['get_time'])
            if self.rule['get_img']:
                imgs = response.xpath(self.rule['get_img']).getall()
                article['image'] = imgs
            self.article_data.append(article)
        elif self.rule['get_img']:
            imgs = response.xpath(self.rule['get_img']).getall()
            print('item ', response.url, len(imgs))
            self.image_data.extend(imgs)
            if time.time() - self.start > 60 * 5:
                self.start = time.time()
                print('共有', len(self.image_data), '个')
                with open(f'D:/python/viewer/src/renderer/src/assets/json_source/{self.rule["name"]}.json', 'w') as f:
                    f.write(json.dumps(self.image_data))

    @staticmethod
    def close(spider, reason):
        with open(f'D:/python/viewer/src/renderer/src/assets/json_source/{spider.rule["name"]}.json', 'w') as f:
            f.write(json.dumps(spider.image_data))
        print('共有', len(spider.data), '个')
        closed = getattr(spider, "closed", None)
        if callable(closed):
            return closed(reason)
