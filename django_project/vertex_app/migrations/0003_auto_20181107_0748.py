# Generated by Django 2.0.1 on 2018-11-07 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vertex_app', '0002_auto_20181106_1934'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subrequest',
            name='type',
        ),
        migrations.AddField(
            model_name='subrequest',
            name='checker_name',
            field=models.CharField(default=0, max_length=100, verbose_name='Назначенная проверка'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='subrequest',
            name='stopwatch',
            field=models.FloatField(blank=True, null=True, verbose_name='Замер'),
        ),
    ]