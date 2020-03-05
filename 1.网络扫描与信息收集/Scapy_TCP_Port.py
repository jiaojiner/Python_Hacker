#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391
# 欢迎留言讨论，共同学习进步！

from scapy.all import *
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
# 思科设备可使用show control-plane host open-ports查看开放端口


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


def syn_scan_final(hostname,lport,hport):
    # 在扫描之前进行ping测试
    ping_result = scapy_ping_one(hostname)
    if ping_result[1] == 2:
        print('设备' + hostname + '不可达！！！')
    else:
        # 发送TCP SYN包
        result_raw = sr(IP(dst=hostname)/
                        TCP(dport=(int(lport), int(hport)), flags="S"),
                        timeout=1,
                        verbose=False)

        result_list = result_raw[0].res  # 类型为清单
        for i in range(len(result_list)):
            # 确认为TCP数据包
            if result_list[i][1].haslayer(TCP):
                TCP_Fields = result_list[i][1].getlayer(TCP).fields
                # 确认为SYN ACK数据包
                if TCP_Fields['flags'] == 18:
                    print('端口号: ' + str(TCP_Fields['sport']) + '  is Open!!!')


if __name__ == '__main__':
    host = input('请输入扫描主机的IP地址: ')
    port_low = input('请输入扫描端口的最低端口号: ')
    port_high = input('请输入扫描端口的最高端口号: ')
    syn_scan_final(host, port_low, port_high)
