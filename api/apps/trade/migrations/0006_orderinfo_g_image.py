# Generated by Django 2.0.7 on 2018-07-24 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trade', '0005_useraddress_postcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderinfo',
            name='g_image',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='商品封面图url'),
        ),
    ]
