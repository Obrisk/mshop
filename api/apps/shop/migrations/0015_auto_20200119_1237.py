# Generated by Django 2.2 on 2020-01-19 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20191205_1656'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qrcode',
            name='device',
        ),
        migrations.RemoveField(
            model_name='qrcode',
            name='shop',
        ),
        migrations.DeleteModel(
            name='Printer',
        ),
        migrations.DeleteModel(
            name='QrCode',
        ),
    ]
