#!/usr/bin/env python3
import requests
from ..stopwatch import stopwatch


@stopwatch
def check(domain_url_or_ip):
    proxies = {
        'http': 'http://195.178.207.241:80',
        'https': 'http://213.87.42.32:52617',
    }
    try:
        response = requests.get(domain_url_or_ip
                         if domain_url_or_ip.startswith('http:') or domain_url_or_ip.startswith(
            'https:') else 'http://%s' % domain_url_or_ip, timeout=10, proxies=proxies)
        if hasattr(response, 'status_code') and response.status_code:
            return 'HTTP STATUS %s CODE RETURNED' % response.status_code
        return 'NO ANY HTTP STATUS CODE RETURNED'
    except (requests.exceptions.Timeout, Exception) as e:
        if e:
            pass
        return 'Exception occur'
