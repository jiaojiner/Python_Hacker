#!/usr/bin/env python3
# -*- encoding = utf-8 -*-
# 该代码由本人学习时编写，仅供自娱自乐！
# 本人QQ：1945962391
# 欢迎留言讨论，共同学习进步！


import platform
import netifaces
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)  # 清除报错


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


if __name__ == "__main__":
    from optparse import OptionParser

    usage = "./ARP_Request ipaddress -i interface"
    version = "version 1.0"
    parser = OptionParser(usage=usage, version=version)
    parser.add_option("-i", "--interface", dest="iface", help="Specify an interface", default='ens160', type="string")
    (options, args) = parser.parse_args()
    if arp_request(args[0], options.iface)[1]:
        print(args[0] + ' 的MAC地址为: ' + arp_request(args[0], options.iface)[1])
    else:
        print('请确认主机:' + args[0] + ' 是否存在')
