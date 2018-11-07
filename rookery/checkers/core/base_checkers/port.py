#!/usr/bin/env python3
import socket
from ..stopwatch import stopwatch


@stopwatch
def check(domain_url_or_ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)
    try:
        result = 'opened' if sock.connect_ex((domain_url_or_ip, port)) == 0 else 'closed'
    except Exception as e:
        result = str(e)
    finally:
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()
    return result
