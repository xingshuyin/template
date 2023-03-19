# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    pub_time = scrapy.Field()
    content = scrapy.Field()
    source = scrapy.Field()
    url_hash = scrapy.Field()
    type = scrapy.Field()
