#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391
# 欢迎留言讨论，共同学习进步！

import nmap
import sys


def nmap_ping_scan(network_prefix):
    # 创建一个扫描实例
    nm = nmap.PortScanner()
    # 配置nmap参数
    ping_scan_raw_result = nm.scan(hosts=network_prefix, arguments='-v -n -sn')
    host_list = []
    # 分析扫描结果,并放入主机清单
    for Result in ping_scan_raw_result['scan'].values():
        if Result['status']['state'] == 'up':
            host_list.append(Result['addresses']['ipv4'])
    return host_list


if __name__ == '__main__':
    for host in nmap_ping_scan('192.168.98.0/24'):
        print('%-20s %5s' % (host, 'is UP'))
