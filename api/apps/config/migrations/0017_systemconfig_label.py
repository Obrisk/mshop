# Generated by Django 2.1.5 on 2019-02-15 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0016_notice_update_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='systemconfig',
            name='label',
            field=models.CharField(max_length=64, null=True, verbose_name='配置名称'),
        ),
    ]