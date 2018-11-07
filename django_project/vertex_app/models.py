from django.db import models

try:
    from django_project.celery_module.celery import app
except:
    from rookery.celery import app
import sys
import os

place = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(place, 'rookery'))
sys.path.insert(1, place)
try:
    from rookery.runner import checkers_queue
except:
    from runner import checkers_queue
import random

# Create your models here.

default_date_format = '%d.%m.%Y %H:%M'


class Request(models.Model):
    class Meta:
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
        ordering = ('-datetime',)

    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    content = models.TextField(blank=False, null=False, verbose_name='Содержание', )
    comment = models.CharField(blank=True, null=True, max_length=50, verbose_name='Комментарий', )

    def __str__(self):
        return 'ID{x}: {y}'.format(x=self.id, y=self.datetime.strftime(default_date_format))

    def save(self, *args, **kwargs):
        super(Request, self).save(*args, **kwargs)
        # Проверочный запрос разбивается на подзапросы (то есть список доменов или ip на отдельные),
        # те сохраняются и исполняются
        # и это присходит в ИНОМ потоке от потока исполнения веба
        save_sub_requests_task.delay(self.pk)

    def save_sub_requests(self):
        import re
        sub_requests_contents = set()
        separators = ['\t', '\n', '\r', ' ', ';']
        separators_str = '|'.join(separators)
        arr = re.split(separators_str, self.content)
        for a in arr:
            sub_requests_contents.add(a.strip(separators_str))

        if len(sub_requests_contents) == 0:
            sub_requests_contents = sub_requests_contents.union(self.content)

        if '' in sub_requests_contents:
            sub_requests_contents.remove('')
        if None in sub_requests_contents:
            sub_requests_contents.remove(None)
        for content in sub_requests_contents:
            SubRequest.save_for_check(self, content)


# @app.task
@app.task(name='save_sub_requests_task')
def save_sub_requests_task(pk):
    request = Request.objects.get(pk=pk)
    request.save_sub_requests()


class SubRequestStatus(models.Model):
    class Meta:
        verbose_name = 'Статус подзапоса'
        verbose_name_plural = 'Статусы подзапосов'
        unique_together = (('code',),)

    code = models.CharField(blank=False, null=False, max_length=10, verbose_name='Код статуса', )
    name = models.CharField(blank=False, null=False, max_length=50, verbose_name='Статус', )

    def __str__(self):
        return self.name


class SubRequestStatuses:
    CREATED = SubRequestStatus.objects.filter(code='created')[:1][0]
    ERROR = SubRequestStatus.objects.filter(code='error')[:1][0]
    PROCESSING = SubRequestStatus.objects.filter(code='processing')[:1][0]
    READY = SubRequestStatus.objects.filter(code='ready')[:1][0]


class SubRequest(models.Model):
    class Meta:
        verbose_name = 'Подзапрос'
        verbose_name_plural = 'Подзапрос'
        ordering = ('content',)
        unique_together = (('content', 'request'),)

    request = models.ForeignKey(
        Request,
        on_delete=models.CASCADE,
        verbose_name=Request._meta.verbose_name.title())
    status = models.ForeignKey(
        SubRequestStatus,
        on_delete=models.CASCADE,
        verbose_name=SubRequestStatus._meta.verbose_name.title())
    checker_name = models.CharField(blank=False, null=False, max_length=100, verbose_name='Назначенная проверка', )
    content = models.CharField(blank=False, null=False, max_length=100, verbose_name='Содержание', )
    stopwatch = models.FloatField(blank=True, null=True, verbose_name='Замер', )
    result = models.TextField(blank=True, null=True, verbose_name='Результат', )
    checker = None

    @staticmethod
    def save_for_check(request, content):
        obj = SubRequest()
        obj.request = request
        obj.content = content
        obj.status = SubRequestStatuses.CREATED
        checker = random.choice(list(checkers_queue.keys()))
        obj.checker_name = '%s.%s' % (checker.__module__, checker.__name__)
        obj.save()
        obj.check_me_by(checker)

    def check_me_by(self, checker):
        self.status = SubRequestStatuses.PROCESSING
        result = checker(self.content)
        self.stopwatch = result[0]
        self.result = result[1]
        self.status = SubRequestStatuses.READY
        self.save()
