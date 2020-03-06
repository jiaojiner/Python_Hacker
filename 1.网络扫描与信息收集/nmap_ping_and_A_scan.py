#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391
# 欢迎留言讨论，共同学习进步！

import nmap
import sys
from nmap_ping_scan import nmap_ping_scan
from nmap_A_scan import nmap_A_scan


def nmap_ping_A_scan(network_prefix):
    hosts = nmap_ping_scan(network_prefix)
    for host in hosts:
        nmap_A_scan(host)


if __name__ == '__main__':
    nmap_ping_A_scan(sys.argv[1])
