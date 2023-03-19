# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from system.models import Article
from scrapy_djangoitem import DjangoItem


class NewsItem(DjangoItem):
    # define the fields for your item here like:
    django_model = Article
