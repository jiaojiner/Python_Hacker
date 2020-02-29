#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391
# 欢迎留言讨论，共同学习进步！

from socket import inet_aton
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
import ipaddress
import multiprocessing
import time
import sys
import struct
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def scapy_ping_one(host):
    packet = IP(dst=host, ttl=1) / ICMP() / b'Welcome'  # 构造Ping数据包
    ping = sr1(packet, timeout=1, verbose=False)  # 获取响应信息，超时为2秒，关闭详细信息
    try:
        if ping.getlayer(IP).fields['src'] == host and ping.getlayer(ICMP).fields['type'] == 0:
            # 如果收到目的返回的ICMP ECHO-Reply包
            return host, 1  # 返回主机和结果，1为通
        else:
            return host, 2  # 返回主机和结果，2为不通
    except Exception:
        return host, 2  # 出现异常也返回主机和结果，2为不通


def sort_ip(ips):
    # inet_aton(ip) 转换IP到直接字符串
    # >>> inet_aton("172.16.1.1")
    # b'\xac\x10\x01\x01'
    # struct.unpack("!L", inet_aton(ip))[0] 把直接字符串转换为整数
    # >>> struct.unpack("!L", inet_aton("172.16.1.1"))
    # (2886729985,)
    # >>> struct.unpack("!L", inet_aton("172.16.1.1"))[0]
    # 2886729985
    # 根据整数排序,然后返回排序后的ips列表
    return sorted(ips, key=lambda ip: struct.unpack("!L", inet_aton(ip))[0])


def scapy_ping_scan(network):
    net = ipaddress.ip_network(network)
    ip_list = []
    for ip in net:
        ip_list.append(str(ip))  # 把IP地址放入ip_list的清单
    pool = multiprocessing.Pool(processes=100)  # 创建多进程的进程池（并发为100）
    result = pool.map(scapy_ping_one, ip_list)  # 关联函数与参数，并且提取结果到result
    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束
    scan_list = []  # 扫描结果IP地址的清单
    for ip_result, ok in result:
        if ok == 1:  # 如果范围值为1
            scan_list.append(ip_result)  # 把IP地址放入scan_list清单里边
    return sort_ip(scan_list)  # 排序并且打印清单


if __name__ == '__main__':
    t1 = time.time()
    print('活动IP地址如下:')
    for ip in scapy_ping_scan(sys.argv[1]):
        print(str(ip))
    t2 = time.time()
    print('本次扫描时间: %.2f' % (t2 - t1))  # 计算并且打印扫描时间
