# -*- coding: utf-8 -*-
import string
import re

import config

#封鎖 IP / Hostname / DNSBL 綜合性檢查
def ban_ip_host_DNSBL_check(ip, host, baninfo):
    if config['BAN_CHECK']:
        return False
    host = string.lower(host)
    check_twice = True if ip != host else False
    is_banned = False
    for pattern in config['BANPATTERN']:
        pass

#反櫻花字
def anti_sakura(s):
    return re.findall('/[\x{E000}-\x{F848}]/u', z)