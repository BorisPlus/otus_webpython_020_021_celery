#!/usr/bin/env python3
import socket
from ..stopwatch import stopwatch


@stopwatch
def check(domain_url_or_ip):
    try:
        ip = socket.gethostbyname(domain_url_or_ip)
        return ip if ip else '*.*.*.*/* :)'
    except Exception as e:
        return str(e)
