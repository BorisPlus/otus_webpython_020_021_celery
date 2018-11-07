# Generated by Django 2.0.1 on 2018-11-07 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vertex_app', '0002_request'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('checker_name', models.CharField(max_length=100, verbose_name='Назначенная проверка')),
                ('content', models.CharField(max_length=100, verbose_name='Содержание')),
                ('stopwatch', models.FloatField(blank=True, null=True, verbose_name='Замер')),
                ('result', models.TextField(blank=True, null=True, verbose_name='Результат')),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vertex_app.Request', verbose_name='Запрос')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vertex_app.SubRequestStatus', verbose_name='Статус Подзапоса')),
            ],
            options={
                'ordering': ('content',),
                'verbose_name': 'Подзапрос',
                'verbose_name_plural': 'Подзапрос',
            },
        ),
        migrations.AlterUniqueTogether(
            name='subrequest',
            unique_together={('content', 'request')},
        ),
    ]
