# Generated by Django 2.1.9 on 2019-09-27 08:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0005_wxuser_upload_prem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wxuser',
            old_name='upload_prem',
            new_name='upload_perm',
        ),
    ]