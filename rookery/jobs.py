import sys
import os
import time
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rookery.app import app


@app.task(name='jobs.say_hello')
def say_hello():
    returned = 'Hi, bro!'
    print(returned)
    return returned


@app.task(name='jobs.do_some_work')
def do_some_work():
    time_to_work = random.choice([5, 10, 15])
    print('I wanna sleep %ssec.' % time_to_work)
    time.sleep(time_to_work)
    return time_to_work


if __name__ == "__main__":
    print('1.', 'say_hello()')
    result = say_hello.delay()
    print('\t', '1.result =', result)
    print()

    print('2.', 'do_some_work()')
    result = do_some_work.delay()
    print('\t', '2.result =', result)
    print('\t', '2.result.ready() =', result.ready())
    print('\t', '2.result.get() =', result.get())
    print()
