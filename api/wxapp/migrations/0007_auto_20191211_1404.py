# Generated by Django 2.1.10 on 2019-12-11 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0006_auto_20190927_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesstoken',
            name='version_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='wxappcode',
            name='version_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='wxsession',
            name='version_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
        migrations.AddField(
            model_name='wxuser',
            name='version_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='更新时间'),
        ),
    ]
