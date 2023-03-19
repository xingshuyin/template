import re
import scrapy
from ..tools import path, deal_path
from ..items import NewsItem


# 文旅部-焦点新闻
class CultureSpider(scrapy.Spider):
    name = 'culture_whyw'
    allowed_domains = ['*']
    start_urls = ['https://www.mct.gov.cn/whzx/whyw/']
    pages = 1

    def start_requests(self):
        yield scrapy.Request(url='https://www.mct.gov.cn/whzx/whyw/', method="GET", callback=self.get_page, dont_filter=True)

    def get_page(self, response):
        page = response.css('*').re(f"var countPage = (\d+);")
        for i in range(int(page[0])):
            url = f"https://www.mct.gov.cn/whzx/whyw/index{'_'+str(i) if i>0 else ''}.htm"
            yield scrapy.Request(url=url, method="GET", callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        print('page ----  ', response.url)
        for line in response.css('.lm_tabe tr'):
            createAt = line.css('.bt_time::text').get()
            url = 'https://www.mct.gov.cn/whzx/whyw' + line.css('a::attr(href)').get().strip('.')
            yield scrapy.Request(url=url, method="GET", callback=lambda r: self.parse(r, createAt), dont_filter=True)

    def parse(self, response, createAt):

        print('item ----  ', response.url)
        # base1 = response.url[:response.url.rindex('/')]
        # base2 = base1[:base1.rindex('/')]
        # base3 = base2[:base2.rindex('/')]
        content = ''.join(response.css('.TRS_Editor').getall())
        cover = response.css('.TRS_Editor').re('<img.*?src="(.*?)".*?>')
        if len(cover) > 0:
            cover = path(cover[0], response)
        else:
            cover = None
        content = deal_path(content, response)
        # content = re.sub(r'<img(.*?)src="(./(.*?))"(.*?)>', f'<img\\1src="{base1}/\\3"\\4>', content)
        # content = re.sub(r'<img(.*?)src="(../(.*?))"(.*?)>', f'<img\\1src="{base2}/\\3"\\4>', content)
        # content = re.sub(r'<img(.*?)src="(../../(.*?))"(.*?)>', f'<img\\1src="{base3}/\\3"\\4>', content)
        name = ''.join(response.css('.sp_title::text').getall()).replace('\n', '').strip() + ''.join(response.css('.sp_title + div::text').getall()).replace('\n', '').strip()
        source = response.css('.phone_zt1::text').get().replace('信息来源：', '').strip()
        item = NewsItem()
        item['name'] = name
        item['category'] = 13
        item['cover'] = cover
        item['url'] = response.url
        item['createAt'] = createAt
        item['content'] = content
        item['source'] = source
        yield item
        # for line in response.css('.lm_tabe tr'):
        #     print(line.css('a::attr(href)').get())
