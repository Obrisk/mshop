# Generated by Django 2.1.7 on 2019-03-25 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0006_turnoversstatistics'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxuserstatistics',
            name='user_total',
            field=models.PositiveIntegerField(default=0, verbose_name='新增用户数量'),
        ),
    ]
