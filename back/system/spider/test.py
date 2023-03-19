import re
import requests

url = 'http://img.hebnews.cn/2020-01/30/10f36e33-8dbc-4c3f-be33-14c12e71dc94_watermark.jpg'
print(requests.get(url, headers={'Referer': 'http://127.0.0.1:5173/'}).status_code)
