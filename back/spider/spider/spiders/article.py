from ..tools import path, deal_path
from ..pipelines import SpiderPipeline
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request, Response, HtmlResponse
from scrapy.linkextractors import LinkExtractor
from hashlib import md5
import pymysql
import re

db = pymysql.connect(
    host="localhost",
    port=3306,
    user='root',  #在这里输入用户名
    password='123456',  #在这里输入密码
    # charset='utf8mb4',
    database='template')  #连接数据库
cursor = db.cursor()


class ArticleSpider(CrawlSpider):  # https://docs.scrapy.org/en/latest/topics/spiders.html#crawlspider
    '''通用爬虫'''
    name = "ArticleSpider"
    pipline = set([SpiderPipeline])

    def __init__(self, rule):
        '''初始化

        Args:
            rule (dict): 爬虫规则
        '''
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
        super(ArticleSpider, self).__init__()

    def parse_start_url(self, response, **kwargs):
        '''判断是否构造分页链接
        '''
        if self.rule['re_page_num']:
            pages = response.css('*').re(self.rule['re_page_num'])  # 正则匹配页码,最终使用第一个匹配到的页数
            if len(pages) > 0:
                for num in range(int(self.rule['start_page_num']), int(pages[0]) + int(self.rule['start_page_num'])):
                    if self.rule['page_format_shift']:
                        num = eval(self.rule['page_format_shift'])
                    yield scrapy.Request(url=self.rule['page_format'].format(num), method="GET", callback=lambda r: self._requests_to_follow(r), dont_filter=True)
        elif self.rule['max_page_num']:
            for num in range(int(self.rule['start_page_num']), self.rule['max_page_num'] + 1):
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
                        print(link.url)
                        yield scrapy.Request(url=link.url, method="GET", callback=lambda r: self._requests_to_follow(r), dont_filter=True)
                    else:
                        pass
                else:

                    cursor.execute(f"select 1 from  `article` where url_hash = '{md5(link.url.encode(encoding='UTF-8')).hexdigest()}' and type=2 limit 1")
                    count = cursor.fetchone()
                    print(count)
                    if count is None:
                        yield scrapy.Request(url=link.url, method="GET", callback=lambda r: self.parse(r), dont_filter=True)

    def parse(self, response):
        '''请求/解析文章详情页
        '''
        pub_time = response.xpath(self.rule['xpath_time'])
        if self.rule['re_time']:
            pub_time = pub_time.re(self.rule['re_time'])
            if len(pub_time) > 0:
                pub_time = pub_time[0].replace('\n', '').strip()
            else:
                pub_time = None
        else:
            pub_time = ''.join(pub_time.getall()).replace('\n', '').strip()
        # content = ''.join(response.xpath(self.rule['xpath_content']).getall()).replace('\n', '').strip()  # 获取文章内容
        content = response.xpath(self.rule['xpath_content']).getall()  # 获取文章内容
        if len(content) == 0:
            print('内容为空', response.url)
            return
        content = content[0].replace('\n', '').strip()
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

        item = {}
        item['url'] = response.url
        item['name'] = name
        item['pub_time'] = pub_time
        item['content'] = content
        item['source'] = source
        item['url_hash'] = md5(item['url'].encode(encoding='UTF-8')).hexdigest()
        item['type'] = 2

        # try:
        #     item.save()
        #     print('保存成功----------', item['url'])
        # except:
        #     close_old_connections()
        #     print('保存失败----------', item['url'])
        print('保存成功----------', item['url'])
        return item
