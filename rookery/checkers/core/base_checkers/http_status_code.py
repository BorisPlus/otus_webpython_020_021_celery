#!/usr/bin/env python3
import requests
from ..stopwatch import stopwatch


@stopwatch
def check(domain_url_or_ip, status_code):
    try:
        proxies = {
            'http': 'http://195.178.207.241:80',
            'https': 'http://213.87.42.32:52617',
        }
        return 'HTTP STATUS %s OK' % status_code if requests.get(
            domain_url_or_ip
            if domain_url_or_ip.startswith('http:') or domain_url_or_ip.startswith(
                'https:') else 'http://%s' % domain_url_or_ip,
            timeout=10,
            proxies=proxies
        ).status_code == status_code else 'HTTP STATUS %s FAIL' % status_code
    except (requests.exceptions.Timeout, Exception) as e:
        if e:
            pass
        return 'NO ANY HTTP STATUS'
