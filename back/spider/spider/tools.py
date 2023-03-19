import re
'''
description: 获取链接几级父级目录
param {*} full_url 提取父级目录的链接
param {*} num 提取级别
return {string} 父级目录
'''


def root_path(full_url, num):
    r = full_url
    for _ in range(num):
        r = r[:r.rindex('/')]
    return r


'''
description: 获取链接完整路径
param {*} url
param {*} response
return {*}
'''


def path(url, response):
    full_url = response.url
    if '../' in url:
        f_path_count = url.count('../')
        root = root_path(full_url, f_path_count + 1)
        p = url.strip('../')
    elif './' in url:
        root = root_path(full_url, 1)
        p = url.strip('./')
    elif url.startswith('/'):
        t = [s.start() for s in re.finditer('/', response.url)]  #TODO: 查找返回索引
        root = response.url[:t[2]]  # 获取网站根目录
        p = url.strip('/')
    else:
        return url
    return root + '/' + p


    # if '../../../' in url:
    #     url = base4 + '/' + url.strip('../')
    # if '../../' in url:
    #     url = base3 + '/' + url.strip('../')
    # elif '../' in url:
    #     url = base2 + '/' + url.strip('../')
    # elif './' in url:
    #     url = base1 + '/' + url.strip('../')
def get_group(a, response, pre):
    # print(a.group(3))
    return pre + path(a.group(1), response) + '"'


'''
description: 处理所有图片链接转换为绝对路径
param {*} content
param {*} response
return {*}
'''


def deal_path(content, response):

    content = re.sub(r'src="(.*?)"', lambda x: get_group(x, response, 'src="'), content)
    content = re.sub(r'href="(.*?)"', lambda x: get_group(x, response, 'href="'), content)
    return content


if __name__ == '__main__':
    content = """
    <p style="text-align: center;"><img src="./W020221026346836975882.jpg" width="600" style="border-width: 0px;" alt="" oldsrc="W020221026346836975882.jpg"></p>
    """
    url = 'https://zwgk.mct.gov.cn/zfxxgkml/503/507/index_3081.html'
    a = [s.start() for s in re.finditer('/', url)]
    print(url[:a[2]])
