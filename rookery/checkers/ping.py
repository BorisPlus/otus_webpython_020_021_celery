#!/usr/bin/env python3
from platform import system as system_name
from .core.base_checkers import subprocess_check_call


def check(domain_url_or_ip):
    parameters = "-n 1" if system_name().lower() == "windows" else "-c 1"
    return subprocess_check_call.check(["ping", parameters, domain_url_or_ip])
