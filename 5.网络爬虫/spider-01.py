#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391 
# 欢迎留言讨论，共同学习进步！

# spider
# 爬虫，spider 网络蜘蛛: 用于数据的网络上数据的采集和抓取，也有人称爬虫为采集机器人

# 爬虫我们学习的过程当中学习俩个阶段
# 初级的爬虫，我们使用python的模块对一些不需要登录的网站数据进行采集和下载
# 模拟登录，我们通过分析http协议对有登录的网站模拟浏览器进行登录
# 我们会涉及到代理(proxy)，递归，多线程，分布式几种常见的爬虫

# 爬虫的步骤
# 分析
# 请求、处理响应
# 数据筛选
# 数据存储

# scrapy 框架

# 框架:
# 当你第一次开发的时候，你完全的将一个项目写下来
# 当你第二次开发同样的项目的时候，你发现第一次开发当中有一部分代码可以复用
# 当你但三次开发的时候，你把第一次二次可以复用的代码进行了封装
# 往复下来你就形成了一个框架
# 框架就是指将一类共性的项目的共性的功能写成一个可以方便复用的大的功能块儿

# 分析
# 分析http请求
# 分析HTML请求
# 分析js、ajax请求
# Firefox
# 开发者工具
# firebug
# httpfox
# 分析抓包
# 请求和响应部分
# 爬虫模块
# urllib
# urllib2
# requests

# httplib
# cookielib
# hashlib
# 数据筛选
# 匹配模块
# re
# lxml xpath
# beautifulsoup bs4
# 数据存储
# mysql
# file #file 日志记录

import re
import urllib.request

from lxml import etree

url = "http://www.heuet.edu.cn/"
hander = {
    "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:73.0) Gecko/20100101 Firefox/73.0"
}
req = urllib.request.Request(url, data=None, headers=hander)
ope = urllib.request.urlopen(req)
content = ope.read()
# print(content.decode())
res = re.findall('<img src="(.*)?"', content.decode())
# print(res)
for i in res:
    urls = i.split("\"")[0]
    img_url = 'http://www.heuet.edu.cn/' + urls
    # print(img_url)
    name = urls.rsplit("/")[1]
    # print(name)
    urllib.request.urlretrieve(img_url, name)

