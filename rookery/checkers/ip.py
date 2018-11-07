#!/usr/bin/env python3
from .core.base_checkers import ip


def check(domain_url_or_ip):
    return ip.check(domain_url_or_ip)
