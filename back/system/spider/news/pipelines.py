# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter

from hashlib import md5
import django
from system.models import Category
import random
import requests
# from django.db import connections
import time

default_cover = {
    12: ['http://121.89.199.142/api/media/cover/hot1.jpg', 'http://121.89.199.142/api/media/cover/hot2.png'],
    14: ['http://121.89.199.142/api/media/cover/notice1.jpg', 'http://121.89.199.142/api/media/cover/notice2.png'],
    13: ['http://121.89.199.142/api/media/cover/news1.jpg', 'http://121.89.199.142/api/media/cover/news2.jpg'],
    15: ['http://121.89.199.142/api/media/cover/media1.png', 'http://121.89.199.142/api/media/cover/media2.png'],
    16: ['http://121.89.199.142/api/media/cover/performance1.jpg', 'http://121.89.199.142/api/media/cover/performance2.jpg'],
}

# current = time.time()

# def close_old_connections():
#     for conn in connections.all():
#         conn.close_if_unusable_or_obsolete()


class NewsPipeline:

    def process_item(self, item, spider):
        # try:
        item['category'] = Category.objects.get(id=item['category'])
        item['url_hash'] = md5(item['url'].encode(encoding='UTF-8')).hexdigest()
        item['type'] = 3
        if not item['cover']:
            item['cover'] = random.choice(default_cover[item['category'].id])
        # else:
        #     if requests.get(item['cover'], headers={'Referer': 'http://127.0.0.1:5173/'}).status_code != 200:  # 尝试跨域请求图片,不行的话就使用随机的图片
        #         item['cover'] = random.choice(default_cover[item['category'].id])
        print('保存----------', item['url'])
        print('保存----------', item['url'])
        item.save()
        # return item

    # except Exception as e:
    #     print('重新连接数据库')
    #     close_old_connections()
    #     item['category'] = Category.objects.get(id=item['category'])
    #     item['url_hash'] = md5(item['url'].encode(encoding='UTF-8')).hexdigest()
    #     item['type'] = 3
    #     if not item['cover']:
    #         item['cover'] = random.choice(default_cover[item['category'].id])
    #     # else:
    #     #     if requests.get(item['cover'], headers={'Referer': 'http://127.0.0.1:5173/'}).status_code != 200:  # 尝试跨域请求图片,不行的话就使用随机的图片
    #     #         item['cover'] = random.choice(default_cover[item['category'].id])
    #     try:
    #         item.save()
    #         print('重新连接数据库后-保存----------', item['url'])
    #     except django.db.utils.IntegrityError:
    #         print('重新连接数据库后-重复----------', item['url'])
    # return item
    # finally:
    #     pass
