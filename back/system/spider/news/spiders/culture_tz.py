import scrapy
import re
from ..tools import path, deal_path
from ..items import NewsItem


# 文旅部-通知
class CultureSpider(scrapy.Spider):
    name = 'culture_tz'
    allowed_domains = ['*']
    start_urls = ['https://zwgk.mct.gov.cn/zfxxgkml/503/508/index_3081.html']
    pages = 1

    def start_requests(self):
        # for i in ['https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081.html','https://zwgk.mct.gov.cn/zfxxgkml/503/510/index_3081.html']
        yield scrapy.Request(url='https://zwgk.mct.gov.cn/zfxxgkml/503/508/index_3081.html', method="GET", callback=self.get_page, dont_filter=True)

    def get_page(self, response):
        page = response.css('*').re(f"var countPage = (\d+)")
        for i in range(int(page[0])):
            url = f"https://zwgk.mct.gov.cn/zfxxgkml/503/508/index_3081{'_'+str(i) if i>0 else ''}.html"
            yield scrapy.Request(url=url, method="GET", callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        print('page ----  ',response.url)
        # base1 = response.url[:response.url.rindex('/')]  #./
        # base2 = base1[:base1.rindex('/')]  # ../
        # base3 = base2[:base2.rindex('/')]  # ../../
        # base4 = base3[:base3.rindex('/')]  # ../../
        for line in response.css('.mesgopen2 li'):
            createAt = line.css('.date::text').get()
            url = line.css('a::attr(href)').get()
            url = path(url, response)
            yield scrapy.Request(url=url, method="GET", callback=lambda r: self.parse(r, createAt), dont_filter=True)

    def parse(self, response, createAt):
        print('utem ----  ',response.url)
        content = ''.join(response.css('.gsj_htmlcon_bot').getall())
        cover = response.css('.gsj_htmlcon_bot').re('<img.*?src="(.*?)".*?>')
        if len(cover) > 0:
            cover = path(cover[0],response)
        else:
            cover = None
        # base1 = response.url[:response.url.rindex('/')]
        # base2 = base1[:base1.rindex('/')]
        # base3 = base2[:base2.rindex('/')]
        content=deal_path(content,response)
        # content = re.sub(r'<img(.*?)src="(./(.*?))"(.*?)>', f'<img\\1src="{base1}/\\3"\\4>', content)
        # content = re.sub(r'<img(.*?)src="(../(.*?))"(.*?)>', f'<img\\1src="{base2}/\\3"\\4>', content)
        # content = re.sub(r'<img(.*?)src="(../../(.*?))"(.*?)>', f'<img\\1src="{base3}/\\3"\\4>', content)

        name = ''.join(response.css('.xxgk_title::text').getall()).replace('\n', '').strip()+''.join(response.css('.xxgk_title + div::text').getall()).replace('\n', '').strip()
        source = '文旅部'

        item = NewsItem()
        item['name'] = name
        item['category'] = 14
        item['cover'] = cover
        item['url'] = response.url
        item['createAt'] = createAt
        item['content'] = content
        item['source'] = source
        yield item
        # for line in response.css('.lm_tabe tr'):
        #     print(line.css('a::attr(href)').get())
