# Вопросы

## Вопрос 1

```bash
cd ./question
celery --config=celeryconfig --loglevel=INFO worker -A app -n n1
```

В конфигурационном файле CELERY, указанном при запуске, имеется:

```python
CELERY_IMPORTS = ("tasks",)
```

В логе запуска вижу

```text
...
[tasks]
  . tasks.do_some_work
  . tasks.say_hello
...
```

Сами задачи (файл _tasks.py_):
* "поздороваться безответно"
* "поздороваться"
* рандомное время "поспать\поработать"

```python
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
```

Вызовы задач (в файле _tasks.py_) таковы:

```python

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
```

Запускаю параллельно во втором терминале: 

```bash
cd ./question
python3 tasks.py
```

В нем лог:

```text
1. print_hello()
SPECIAL PRINT FROM "print_hello" TASK: Hi, bro!
         1.result = None

2. return_hello()
SPECIAL PRINT FROM "return_hello" TASK: Hi, bro!
         2.result = Hi, bro!

3. do_some_work()
SPECIAL PRINT FROM "do_some_work" TASK: I wanna sleep 5sec.
         3.result = 5

4. do_some_work.delay()
         4.result = f7d551cd-6f0b-49b2-9ba9-6db39a84cdbf
         4.result.ready() = False
         4.result.get() = 10
```

OK.

Но лог в первом терминале:

```text
[2018-11-06 01:04:24,769: INFO/MainProcess] Received task: tasks.do_some_work[f7d551cd-6f0b-49b2-9ba9-6db39a84cdbf]  
[2018-11-06 01:04:24,771: INFO/ForkPoolWorker-4] SPECIAL PRINT FROM "do_some_work" TASK:
[2018-11-06 01:04:24,771: INFO/ForkPoolWorker-4] I wanna sleep 10sec.
[2018-11-06 01:04:34,818: INFO/ForkPoolWorker-4] Task tasks.do_some_work[f7d551cd-6f0b-49b2-9ba9-6db39a84cdbf] succeeded in 10.046968934999768s: 10

```
**Вопрос**: мне уже не понятно, почему в лог WORKER'а попала только последняя задача, и как это связанно c delay(). Как иметь лог всех?

**Ответ получен**: "Чтобы воспользоваться фоновым обработчиком, необходимо использовать метод .delay. При помощи этого метода мы передаем выполнение функции обработчику celery и функция должна сразу же вернуть нас в консоль без каких-либо задержек."

**Вопрос**: то есть всем объявленным методам для Celery нужно будет вписывать ".delay"?

### Вопрос 2

Переименуем файл tasks.py, например, в jobs.py. И сделаем

```python
CELERY_IMPORTS = ("jobs",)
```

Запустим

```bash
cd ./question
celery --config=celeryconfig --loglevel=INFO worker -A app -n n1
```

Я **вижу**, что задачи теперь импортируются по логу как

```text
[tasks]
  . jobs.do_some_work
  . jobs.print_hello
  . jobs.return_hello

```
Но если теперь во втором терминале вызвать 
```bash
python3 jobs.py 
```

То будет получено исключение

```text
1. print_hello()
SPECIAL PRINT FROM "print_hello" TASK: Hi, bro!
         1.result = None

2. return_hello()
SPECIAL PRINT FROM "return_hello" TASK: Hi, bro!
         2.result = Hi, bro!

3. do_some_work()
SPECIAL PRINT FROM "do_some_work" TASK: I wanna sleep 10sec.
         3.result = 10

4. do_some_work.delay()
         4.result = a8e8868f-1a48-4146-9e01-734af404b8f0
         4.result.ready() = True
Traceback (most recent call last):
  File "jobs.py", line 54, in <module>
    print('\t', '4.result.get() =', result.get())
  File "/usr/local/lib/python3.4/dist-packages/celery/result.py", line 213, in get
    self.maybe_throw(callback=callback)
  File "/usr/local/lib/python3.4/dist-packages/celery/result.py", line 329, in maybe_throw
    self.throw(value, self._to_remote_traceback(tb))
  File "/usr/local/lib/python3.4/dist-packages/celery/result.py", line 322, in throw
    self.on_ready.throw(*args, **kwargs)
  File "/usr/local/lib/python3.4/dist-packages/vine/promises.py", line 217, in throw
    reraise(type(exc), exc, tb)
  File "/usr/local/lib/python3.4/dist-packages/vine/five.py", line 179, in reraise
    raise value
celery.exceptions.NotRegistered: 'tasks.do_some_work'

```
А в окне терминала worker'а будет:

```text
[2018-11-06 01:18:10,086: ERROR/MainProcess] Received unregistered task of type 'tasks.do_some_work'.
The message has been ignored and discarded.

Did you remember to import the module containing this task?
Or maybe you're using relative imports?

Please see
http://docs.celeryq.org/en/latest/internals/protocol.html
for more information.

The full contents of the message body was:
'[[], {}, {"chain": null, "errbacks": null, "chord": null, "callbacks": null}]' (77b)
Traceback (most recent call last):
  File "/usr/local/lib/python3.4/dist-packages/celery/worker/consumer/consumer.py", line 558, in on_task_received
    strategy = strategies[type_]
KeyError: 'tasks.do_some_work'

```

**Вопрос**: почему он ищет `tasks.do_some_work`, ведь импорт он делал другого, и вообще, задачи можно помещать не только в единый tasks.py?

