#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391 
# 欢迎留言讨论，共同学习进步！


import re
import urllib.request
from lxml import etree


# 设置url
url = "http://business.sohu.com/20161015/n470353142.shtml"
# url = "http://www.qiushibaike.com/"
# 设置头部
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.04"
}
# 发起请求
# req = urllib2.Request(header,data = None,)
req = urllib.request.Request(url, data=None, headers=header)
# 接收响应
ope = urllib.request.urlopen(req)
# print(ope)
# print(ope.read().decode())
# for i in ope.readlines():
#    print(i.decode())
ope.close()
econtent = etree.HTML(ope.read().decode())  # 构建xpath 树状结构
# xpath 匹配语法
# // 是代表所有的
# /  代表层级
# [] 筛选
# @ 筛选条件
# xpath 匹配到的内容我们又三个方法
# tag 返回对象标签名称
# attrib 返回对象属性
# text 返回对象当中的文本

# myx = econtent.xpath("//div")
# print(myx)
myx = econtent.xpath("//p")

for i in myx:
    # print(i.tag)
    # print(i.attrib)
    print(i.text)

