# Generated by Django 2.1.5 on 2019-02-15 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='file_type',
            field=models.CharField(choices=[('video', '视频'), ('picture', '图片'), ('audio', '音频')], default='picture', max_length=128, verbose_name='素材类型'),
        ),
    ]
