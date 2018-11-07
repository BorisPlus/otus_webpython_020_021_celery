#!/usr/bin/env python3
import os
import random
import sys

from redis import Redis
from rq import Queue

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_path not in sys.path:
    sys.path.append(project_path)

from checkers import (
    ping,  # Проверка на PING
    http_any_status_code,  # Проверка на наличие любого статуса HTTP
    http_status_code_200,  # Проверка на 200 код статуса HTTP
    http_status_code_404,  # Проверка на 404 код статуса HTTP
    http_status_code_500,  # Проверка на 500 код статуса HTTP
    port_22,  # Проверка на вероятный SSH
    port_80,  # Проверка на вероятный HTTP
    port_443,  # Проверка на вероятный HTTPS
    ip,  # Проверка IP
)

from check_list import domains_or_ip

redis_conn = Redis()

# проверочные очереди
ping_q = Queue(
    'ping',
    connection=redis_conn)  # Очередь проверки пингов
port_q = Queue(
    'port',
    connection=redis_conn)  # Очередь проверки открытых портов
http_q = Queue(
    'http',
    connection=redis_conn)  # Очередь проверки HTTP статусов

# checkers = [
#     ping.check,
#
#     http_any_status_code.check,
#     http_status_code_200.check,
#     http_status_code_404.check,
#     http_status_code_500.check,
#
#     port_22.check,
#     port_80.check,
#     port_443.check,
# ]

# сопоставление функции проверки и ее очереди
checkers_queue = {
    ping.check: ping_q,
    ip.check: ping_q,

    http_any_status_code.check: http_q,
    http_status_code_200.check: http_q,
    http_status_code_404.check: http_q,
    http_status_code_500.check: http_q,

    port_22.check: port_q,
    port_80.check: port_q,
    port_443.check: port_q,
}

# выборка случайного списка кандидатов на проверку
check_list = random.sample(domains_or_ip, 500)
while len(check_list):
    # выборка случайного кандидата на проверку
    check_item = random.choice(check_list)
    check_list.remove(check_item)
    # выборка случайной функции проверки
    checker = random.choice(list(checkers_queue.keys()))
    # помещение в соответствующую очередь
    result = checkers_queue.get(checker).enqueue(checker, check_item)
