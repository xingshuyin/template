import zmail
server = zmail.server('15631177345@163.com', 'PUQNQSWWLUERDKKG')
with open(r"C:\Users\xingshuyin\Desktop\5.1   栈 - Hello 算法.html", 'r', encoding='utf-8') as f:
    content = f.read()
#  recipients 接收人   cc 抄送人
server.send_mail(recipients=['389656169@qq.com', '15631177345@163.com'], cc=[],
                 mail={'subject': 'Hello!', 'content_text': 'By zmail.', 'content_html': content})


# Retrieve mail
# latest_mail = server.get_latest()
# latest_mail = server.get_headers()
# print(latest_mail)
# zmail.show(latest_mail)
