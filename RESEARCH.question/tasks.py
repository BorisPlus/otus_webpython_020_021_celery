import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rookery.app import app


# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# from app import app

@app.task
def print_hello():
    returned = 'Hi, bro!'
    print('SPECIAL PRINT FROM "print_hello" TASK:', returned)


@app.task
def return_hello():
    returned = 'Hi, bro!'
    print('SPECIAL PRINT FROM "return_hello" TASK:', returned)
    return returned


@app.task
def do_some_work():
    time_to_work = random.choice([5, 10, 15])
    print('SPECIAL PRINT FROM "do_some_work" TASK:', 'I wanna sleep %ssec.' % time_to_work)
    time.sleep(time_to_work)
    return time_to_work


if __name__ == "__main__":
    print('1.', 'print_hello()')
    result = print_hello()
    print('\t', '1.result =', result)
    print()

    print('2.', 'return_hello()')
    result = return_hello()
    print('\t', '2.result =', result)
    print()

    print('3.', 'do_some_work()')
    result = do_some_work()
    print('\t', '3.result =', result)
    print()

    print('4.', 'do_some_work.delay()')
    result = do_some_work.delay()
    print('\t', '4.result =', result)
    print('\t', '4.result.ready() =', result.ready())
    print('\t', '4.result.get() =', result.get())
