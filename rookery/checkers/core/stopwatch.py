#!/usr/bin/env python3
import time


def stopwatch(function_to_decorate):
    def wrapper(*args, **kwargs):
        started_at = time.time()
        result = function_to_decorate(*args, **kwargs)
        ended_at = time.time()
        return (ended_at - started_at), result
    return wrapper
