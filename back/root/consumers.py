import json
from channels.exceptions import InvalidChannelLayerError, AcceptConnection, DenyConnection
from channels.generic.websocket import AsyncJsonWebsocketConsumer

# self.scope
# scope = {'type': 'websocket',  # 协议类型
#          'path': '/ws/group/2/',  # 访问地址
#          'raw_path': b'/ws/group/2/',
#          'headers': [(b'host', b'127.0.0.1:8000'), (b'connection', b'Upgrade'), (b'pragma', b'no-cache'),
#                      (b'cache-control', b'no-cache'), (b'user-agent',
#                                                        b'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.30'),
#                      (b'upgrade', b'websocket'), (b'origin',
#                                                   b'http://127.0.0.1:8000'),
#                      (b'sec-websocket-version',
#                       b'13'), (b'accept-encoding', b'gzip, deflate, br'),
#                      (b'accept-language', b'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'), (b'cookie',
#                                                                                                 b'csrftoken=UGPZ42LfQW4zNWk7PRfl99SQjcO31Sd3VxwpfaemC2BHNfaunMJDOaGEHodNo9JW; sessionid=ud440kh2pyat2yayoqoz34yx0f54bvft'),
#                      (b'sec-websocket-key', b'MJstdH1WPn2+QjIPAnfjKA=='),
#                      (b'sec-websocket-extensions', b'permessage-deflate; client_max_window_bits')],
#          'query_string': b'',
#          'client': ['127.0.0.1', 50977],  # 客户端
#          'server': ['127.0.0.1', 8000],  # 服务器
#          'subprotocols': [],
#          'asgi': {'version': '3.0'},  # asgi版本
#          'cookies': {'csrftoken': 'UGPZ42LfQW4zNWk7PRfl99SQjcO31Sd3VxwpfaemC2BHNfaunMJDOaGEHodNo9JW',
#                      'sessionid': 'ud440kh2pyat2yayoqoz34yx0f54bvft'},  # cookie
#          'session': '<django.utils.functional.LazyObject object at 0x000002111B742130>',  # session
#          'path_remaining': '',
#          'url_route': {'args': (), 'kwargs': {'chat_id': '2'}},  # 路由参数
#          }

consumers = {}


class ChatConsumer(AsyncJsonWebsocketConsumer):
    # 创建consumer  继承AsyncConsumer的类必须所有方法用 async def 定义, 继承SyncConsumer的就用 def 定义
    group = None
    user = None

    async def connect(self):  # 重写方法, 创建连接
        # print('连接上了')
        self.group = self.scope['url_route']['kwargs']['group']  # group就相当于群号
        self.user = self.scope['url_route']['kwargs']['user']
        # 向组(self.table)里添加一个channel连接(self.channel_name),
        await self.channel_layer.group_add(self.group, self.channel_name)
        # self.channel_layer(Consumer实例的指针), self.table(组名), self.channel_name(通道名称)
        consumers['user'] = self
        await self.accept()  # 返回接受连接的信息

    async def disconnect(self, close_code):  # 断开连接
        # 从组中移除channel
        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data=None, bytes_data=None, **kwargs):  # 消息接收器
        # 根据消息的不同参数,用不同的消息发送器,发送不同的消息
        data = {'message': text_data, 'user': self.user}
        # print(data)
        # 向组发送消息
        # 接受前端发送的消息,然后传给发送器
        await self.channel_layer.group_send(self.group, {'type': 'group.message', 'data': data})
        # type消息类型(决定把消息给那个函数), 会把结果返给对应类型名字的函数, 即不同的type不同的发送器 名字中的.会被替换为_

    # 'type': 'message' 的消息发送器  # event 消息接收器接收到的消息
    async def group_message(self, event):
        data = event['data']  # send_json是把数据json话, 而不是需要传入json格式数据
        await self.send_json(data)  # 发送格式化消息为json格式后,传给前端的接收器
