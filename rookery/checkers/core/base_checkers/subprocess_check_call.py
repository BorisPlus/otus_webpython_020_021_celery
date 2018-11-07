#!/usr/bin/env python3
import subprocess
from ..stopwatch import stopwatch


@stopwatch
def check(command_with_args=list(), **kwargs):
    try:
        return 'OK' if subprocess.check_call(command_with_args, **kwargs) == 0 else 'FAIL'
        # return subprocess.check_call(command_with_args, stdout=subprocess.DEVNULL)
        # return subprocess.check_output(command_with_args, timeout=2)
    except Exception as e:
        if e:
            print(e)
            pass
        return None
