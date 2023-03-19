import scrapy
import re
from ..tools import path, deal_path
from ..items import NewsItem


# 河北文旅厅-展演信息
class CultureSpider(scrapy.Spider):
    name = 'culture_hb_zyxx'
    allowed_domains = ['*']
    start_urls = ['https://www.hebeitour.gov.cn/xwzx/zyxx/index.html']
    pages = 1

    def start_requests(self):
        # for i in ['https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081.html','https://zwgk.mct.gov.cn/zfxxgkml/503/510/index_3081.html']
        yield scrapy.Request(url='https://www.hebeitour.gov.cn/xwzx/zyxx/index.html', method="GET", callback=self.get_page, dont_filter=True)

    def get_page(self, response):
        page = response.css('*').re(f"ele\.value>(\d+)\)")
        # for i in range(1, int(page[0])+1):
        for i in range(1, int(page[0]) + 1):
            if i > 3:
                url = f"https://www.hebeitour.gov.cn/zwf/ui/catalog/15937/pc/index_{str(i)}.html"
            else:
                url = f"https://www.hebeitour.gov.cn/xwzx/zyxx/index{'_'+str(i) if i>1 else ''}.html"
            yield scrapy.Request(url=url, method="GET", callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        print('page ----  ',response.url)
        # base1 = response.url[:response.url.rindex('/')]  #./
        # base2 = base1[:base1.rindex('/')]  # ../
        # base3 = base2[:base2.rindex('/')]  # ../../
        # base4 = base3[:base3.rindex('/')]  # ../../
        for line in response.css('.list li'):
            createAt = line.css('span::text').get()
            url = line.css('a::attr(href)').get()
            url = path(url, response)
            yield scrapy.Request(url=url, method="GET", callback=lambda r: self.parse(r, createAt), dont_filter=True)

    def parse(self, response, createAt):
        print('item ----  ',response.url)
        content = ''.join(response.css('#content').getall())
        cover = response.css('#content').re('<img.*?src="(.*?)".*?>')
        if len(cover) > 0:
            cover = path(cover[0],response)
        else:
            cover = None
        # base1 = response.url[:response.url.rindex('/')]
        # base2 = base1[:base1.rindex('/')]
        # base3 = base2[:base2.rindex('/')]
        content=deal_path(content,response)
        # content = ''.join(response.css('.TRS_Editor').getall())
        # content = re.sub(r'<img(.*?)src="(./(.*?))"(.*?)>', f'<img\\1src="{base1}/\\3"\\4>', content)
        # content = re.sub(r'<img(.*?)src="(../(.*?))"(.*?)>', f'<img\\1src="{base2}/\\3"\\4>', content)
        # content = re.sub(r'<img(.*?)src="(../../(.*?))"(.*?)>', f'<img\\1src="{base3}/\\3"\\4>', content)

        name = ''.join(response.css('.content>h1::text').getall()).replace('\n', '').strip()
        source = ''.join(response.css('.post_source::text').getall()).replace('\n', '').strip()
        if '：' in source:
            source = source[source.index('：') + 1:]
        item = NewsItem()
        item['name'] = name
        item['category'] = 16
        item['cover'] = cover
        item['url'] = response.url
        item['createAt'] = createAt
        item['content'] = content
        item['source'] = source
        yield item
        # for line in response.css('.lm_tabe tr'):
        #     print(line.css('a::attr(href)').get())
