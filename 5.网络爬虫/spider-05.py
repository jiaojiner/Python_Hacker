# coding:gbk

import re
import urllib.request
from time import sleep

from lxml import etree
from bs4 import BeautifulSoup

# �ַ�����ƥ�䷽ʽ(�߼����ַ�������ʽ)
# ����:
# ƥ������
# ɸѡ����
# ƥ��ķ�ʽ��
# �������ݹ����﷨������ƥ��
# re
# �������ݹ����̶��ṹ��ƥ��
# lxml
# bs4


# ����������ͼƬ��ȡ
# ��ȡͼƬʵ���������������������ͼƬ��Դ
"""
def fun(a, b, c):
    # a ���صĴ���
    # b ��λ���ش�С
    # c �ܵĴ�С

    num = 1.0 * a * b / c
    if num > 1:
        num = 1
    print("%.3f%%" % (num * 100))


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Referer": "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
}
url = "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
req = urllib.request.Request(url, data=None, headers=header)  # ����header�����������
ope = urllib.request.urlopen(req)  # ���շ������ķ���
content = ope.read().decode()  # �����ص����ݶ�����
# print(content)
html = etree.HTML(content)  # ���ַ��������ݹ�����html�ṹ
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
    req = urllib.request.Request(url, data=None, headers=header)  # ����header�����������
    ope = urllib.request.urlopen(req)  # ���շ������ķ���
    content = ope.read().decode()  # �����ص����ݶ�����
    html = etree.HTML(content)  # ���ַ��������ݹ�����html�ṹ
    xpath = html.xpath("//img")  # ����������ڼ����һҳ�Ƿ�������Ҫ��ͼƬ
    if xpath == False:
        return "https://www.ivsky.com/tupian/the_dead_sea_v57891/"
    else:
        url = xpath.find
        return digui_spider(url)
