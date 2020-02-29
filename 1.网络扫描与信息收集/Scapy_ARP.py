#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391
# 欢迎留言讨论，共同学习进步！

import ipaddress
import multiprocessing
import platform
import struct
import netifaces
from dns.ipv4 import inet_aton
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def get_connection_name_from_guid(iface_guids):  # 获取接口名称
    if platform.system() == "Windows":
        import winreg as wr
        # 产生接口名字清单,默认全部填写上'(unknown)'
        iface_names = ['(unknown)' for i in range(len(iface_guids))]
        # 打开"HKEY_LOCAL_MACHINE"
        reg = wr.ConnectRegistry(None, wr.HKEY_LOCAL_MACHINE)
        # 打开r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}'
        #
        reg_key = wr.OpenKey(reg, r'SYSTEM\CurrentControlSet\Control\Network\{4d36e972-e325-11ce-bfc1-08002be10318}')
        for i in range(len(iface_guids)):
            try:
                # 尝试读取每一个接口ID下对应的Name
                reg_subkey = wr.OpenKey(reg_key, iface_guids[i] + r'\Connection')
                # 如果存在Name,就按照顺序写入iface_names
                iface_names[i] = wr.QueryValueEx(reg_subkey, 'Name')[0]
            except FileNotFoundError:
                pass
        # 把iface_guids, iface_names 压在一起返回
        return zip(iface_guids, iface_names)


def get_ifname(ifname, ni=None):
    if platform.system() == "Linux":
        return ifname
    elif platform.system() == "Windows":
        import winreg as wr
        x = ni.interfaces()
        for i in get_connection_name_from_guid(x):
            # 找到名字所对应的接口ID并返回
            if i[1] == ifname:
                return i[0]
    else:
        print('操作系统不支持,本脚本只能工作在Windows或者Linux环境!')


def get_mac_address(ifname):  # 获取接口MAC地址
    return netifaces.ifaddresses(get_ifname(ifname))[netifaces.AF_LINK][0]['addr']


def get_ip_address(ifname):  # 获取接口ip地址
    return netifaces.ifaddresses(get_ifname(ifname))[netifaces.AF_INET][0]['addr']


def get_ipv6_address(ifname):  # 获取接口ipv6地址
    return netifaces.ifaddresses(get_ifname(ifname))[netifaces.AF_INET6][0]['addr']


def arp_request(ip_address, ifname='ens33'):
    # 获取本机IP地址
    localip = get_ip_address(ifname)['ip_address']
    # 获取本机MAC地址
    localmac = get_mac_address(ifname)
    try:  # 发送ARP请求并等待响应
        result_raw = srp(Ether(src=localmac, dst='FF:FF:FF:FF:FF:FF') /
                         ARP(op=1, hwsrc=localmac, hwdst='00:00:00:00:00:00', psrc=localip, pdst=ip_address),
                         iface=ifname,
                         timeout=1,
                         verbose=False)
        # 把响应的数据包对，产生为清单
        result_list = result_raw[0].res
        # [0]第一组响应数据包
        # [1]接受到的包，[0]为发送的数据包
        # 获取ARP头部字段中的['hwsrc']字段，作为返回值返回
        return ip_address, result_list[0][1].getlayer(ARP).fields['hwsrc']
    except IndexError:
        return ip_address, None


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


def scapy_arp_scan(network):
    net = ipaddress.ip_network(network)
    ip_list = []
    for ip in net:
        ip_list.append(str(ip))  # 把IP地址放入ip_list的清单
    pool = multiprocessing.Pool(processes=100)  # 创建多进程的进程池（并发为100）
    result = pool.map(arp_request, ip_list)  # 关联函数与参数，并且提取结果到result
    pool.close()  # 关闭pool，不在加入新的进程
    pool.join()  # 等待每一个进程结束
    scan_list = []  # 扫描结果IP地址的清单
    for ip, ok in result:
        if ok is None:  # 如果没有获得MAC，就continue进入下一次循环
            continue
        scan_list.append(ip)  # 如果获得了MAC，就把IP地址放入scan_list清单
    return sort_ip(scan_list)  # 排序并且返回清单


if __name__ == '__main__':
    import time
    import sys
    t1 = time.time()
    print('活动IP地址如下:')
    for ip in scapy_arp_scan(sys.argv[1]):
        print(str(ip))
    t2= time.time()
    print('本次扫描时间: %.2f' % (t2-t1))  # 计算并且打印扫描时间
