# Generated by Django 2.1.2 on 2018-12-06 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0014_level_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='level',
            name='discount',
            field=models.PositiveSmallIntegerField(default=100, help_text='%', verbose_name='折扣'),
        ),
    ]
