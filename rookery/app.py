from celery import Celery

app = Celery('rookery')
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'
# app = Celery('rookery', broker='amqp://guest@localhost//')
# app = Celery('tasks', backend='amqp', broker='amqp://guest@127.0.0.1:5672//')
# app = Celery('tasks', backend='amqp', broker='amqp://127.0.0.1:5672//')
# app = Celery('tasks', backend='amqp', broker='amqp://guest:guest@127.0.0.1:5672//')
# app = Celery('tasks', backend='amqp', broker='amqp://')
# RedisSentinel ??
