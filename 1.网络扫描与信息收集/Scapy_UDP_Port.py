#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391 
# 欢迎留言讨论，共同学习进步！

from scapy.all import *
from Scapy_Ping import scapy_ping_one
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
# 思科设备可使用show control-plane host open-ports查看开放端口


def udp_port(host, low_port, high_port):
    ping_result = scapy_ping_one(host)
    if ping_result[-1] == 2:
        print('目标主机不可达！请检查网络环境是否正常')
    else:
        result = sr(IP(dst=host)/UDP(dport=(int(low_port), int(high_port))), timeout=2, verbose=False)
        scan_port = []
        for x in range(int(low_port), int(high_port)):
            scan_port.append(x)
        scan_port_notopen = []
        result_list = result[0].res
        for i in range(len(result_list)):
            if result[i][1].haslayer(ICMP):
                scan_port_notopen.append(result[i][1][3].fiedls['dport'])
        return list(set(scan_port).difference(set(scan_port_notopen)))


if __name__ == '__main__':
    host = input('请输入需要扫描的主机IP地址：')
    low = input('请输入需要扫描的最低端口号：')
    high = input('请输入需要扫描的最高端口号：')
    print('主机', host, '开放的端口号如下：')
    for port in udp_port(host, low, high):
        print(port)
