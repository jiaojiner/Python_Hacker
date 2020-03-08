# coding:gbk

import re
import urllib.request
from time import sleep

from lxml import etree
from bs4 import BeautifulSoup

# 字符串的匹配方式(高级的字符串处理方式)
# 作用:
# 匹配内容
# 筛选内容
# 匹配的方式：
# 按照内容构建语法描述来匹配
# re
# 按照内容构建固定结构来匹配
# lxml
# bs4


# 基本的爬虫图片爬取
# 爬取图片实际上是向服务器请求下载图片资源
"""
def fun(a, b, c):
    # a 下载的次数
    # b 单位下载大小
    # c 总的大小

    num = 1.0 * a * b / c
    if num > 1:
        num = 1
    print("%.3f%%" % (num * 100))


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Referer": "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
}
url = "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
req = urllib.request.Request(url, data=None, headers=header)  # 带着header来请求服务器
ope = urllib.request.urlopen(req)  # 接收服务器的返回
content = ope.read().decode()  # 将返回的内容读出来
# print(content)
html = etree.HTML(content)  # 将字符串的内容构建出html结构
xpath = html.xpath("//div[@class='il_img']/a/img")
for i in xpath:
    # print(i.attrib["src"])
    src = i.attrib["src"]
    src_new = 'http:' + src
    # print(src_new)
    name = src.rsplit("/", 1)
    print("%s is start" % name[1])
    # urllib.request.urlretrieve(src_new, name[1])
    urllib.request.urlretrieve(src_new, name[1], fun)
    print("%s is done" % name[1])
"""


# def fun(num):
#     if num > 10:
#         return num
#     else:
#         return fun(num + 1) + num
#
#
# print(fun(5))


def digui_spider(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
        "Referer": "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
    }
    url = "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
    req = urllib.request.Request(url, data=None, headers=header)  # 带着header来请求服务器
    ope = urllib.request.urlopen(req)  # 接收服务器的返回
    content = ope.read().decode()  # 将返回的内容读出来
    html = etree.HTML(content)  # 将字符串的内容构建出html结构
    xpath = html.xpath("//img")  # 这个代码是在检查下一页是否有我们要的图片
    if xpath == False:
        return "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
    else:
        url = xpath.find
        return digui_spider(url)
