import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rookery.app import app


@app.task(name='jobs.return_goodbuy')
def return_goodbuy():
    returned = 'Goodbay, bro!'
    print('SPECIAL PRINT FROM "return_goodbuy" TASK:', returned)
    return returned


if __name__ == "__main__":

    print('1.', 'return_goodbuy.delay()')
    result = return_goodbuy.delay()
    print('\t', '1.result =', result)
    print('\t', '1.result.ready() =', result.ready())
    print('\t', '1.result.get() =', result.get())
