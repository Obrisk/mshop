# Generated by Django 2.2.1 on 2019-06-19 10:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0026_wechatconfig'),
    ]

    operations = [
        migrations.CreateModel(
            name='DatetimeConfig',
            fields=[
            ],
            options={
                'verbose_name': '时间式配置项',
                'verbose_name_plural': '时间式配置项',
                'proxy': True,
                'indexes': [],
            },
            bases=('config.systemconfig',),
        ),
    ]
