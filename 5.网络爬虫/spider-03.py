# coding:gbk

import re
import urllib.request
from time import sleep

from lxml import etree
from bs4 import BeautifulSoup

# ����ģ�������
# ���������������Ĳ���
# 1��ȷ�������λ�ã�����������˵�ĵ�ַҲ����url
# 2����ʼ����
# header
# user_agent:����û������
# python 2.7
# ���ǽ��Լ�αװ�������

# 3���������������
# 4����Ӧͷ��
# 5����Ӧ����

#
# url = "http://www.xs84.me/"
# url = "http://www.xs84.me/210329_0/"
# header = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
#     "Referer": "http://www.xs84.me/"
# }
# # # header ���ֺ� proxy_ip���������ʹ��random
# #
# # # ��������
# # req = urllib.request.Request(url, data=None, headers=header)
# # # ������Ӧ
# # ope = urllib.request.urlopen(req)
# # # �鿴��ҳ���뷽ʽ����console��document.charset
# # # print(ope.read().decode("gbk"))
# # econtent = etree.HTML(ope.read().decode("gbk"))  # ����xpath ��״�ṹ
# # ope.close()
# # dl_list = econtent.xpath("//dl/dd/a")
# # for dl in dl_list:
# #     # pass
# #     print(dl.attrib['href'])
# #     print(dl.text)
#
#
# # Referer http://www.xs84.me/210329_0/
# url = "http://www.xinxs84.com/210329_21221886/"
# header["Referer"] = "http://www.xs84.me/210329_0/"
# req = urllib.request.Request(url, data=None, headers=header)
# ope = urllib.request.urlopen(req)
# content = ope.read().decode("gbk").replace("<br>", "\n").replace("<br />", "\n")
# # print(content)
# # content_new = content.replace("<br>", "\n").replace("<br/>", "\n")
# # print(content_new)
# content = etree.HTML(content)
# dl_list = content.xpath("//div[@id='content']")
# for i in dl_list:
#     print(i.text)
#     # f = open('1.txt', "w")
#     # f.write(i.text)
#     # f.close()
#     # sleep(1)
# # <div id="content">

"""
# print(dl.attrib["href"])
# print(dl.text)
# xpath ƥ���﷨
# // �Ǵ������е�
# /  ����㼶
# [] ɸѡ
# @ ɸѡ����
# xpath ƥ�䵽��������������������
# tag ���ض����ǩ����
# attrib ���ض�������
# text ���ض����е��ı�

# myx = econtent.xpath("//div")
# myx = econtent.xpath("//p")

# for i in myx:
# print(i.tag)
# print(i.attrib)
#    print(i.text)
# for i in ope.readlines():
#    print(i)
# ope.close()

"""
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Referer": "http://www.xs84.me/"
}


def get_content(url, filename):
    print("%s is start" % filename)
    url = "http://www.xs84.me" + url
    filename = filename + ".txt"

    header["Referer"] = "http://www.xs84.me/210329_0/"
    req = urllib.request.Request(url, data=None, headers=header)
    ope = urllib.request.urlopen(req)
    content = ope.read().decode("gbk")
    content = content.replace("<br>", "\n").replace("<br />", "\n")
    econtent = etree.HTML(content)
    dl_list = econtent.xpath("//div[@id='content']")
    for i in dl_list:
        # print(i.text)
        f = open(filename, "w")
        f.write(i.text)
        f.close()
        sleep(1)
    print("%s is done" % filename)


url = "http://www.xs84.me/210329_0/"

req = urllib.request.Request(url, data=None, headers=header)
ope = urllib.request.urlopen(req)
econtent = etree.HTML(ope.read().decode("gbk"))
dl_list = econtent.xpath("//dl/dd/a")
for dl in dl_list:
    # print(dl.attrib["href"])
    get_content(dl.attrib["href"], dl.text)
