#!/usr/bin/env python3
# import os
# import sys
#
# project_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# if project_path not in sys.path:
#     sys.path.append(project_path)

from .core.base_checkers import http_status_code


def check(domain_url_or_ip):
    return http_status_code.check(domain_url_or_ip, 500)
