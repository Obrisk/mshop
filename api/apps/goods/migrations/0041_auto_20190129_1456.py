# Generated by Django 2.1.5 on 2019-01-29 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qfile', '0001_initial'),
        ('goods', '0040_attach'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attach',
            options={'ordering': ('index',), 'verbose_name': '商品自定义字段', 'verbose_name_plural': '商品自定义字段'},
        ),
        migrations.AddField(
            model_name='attach',
            name='help_text',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='提示说明'),
        ),
        migrations.AddField(
            model_name='attach',
            name='index',
            field=models.PositiveSmallIntegerField(default=1, verbose_name='排序'),
        ),
        migrations.AddField(
            model_name='attach',
            name='is_required',
            field=models.BooleanField(default=False, verbose_name='是否必填'),
        ),
        migrations.AddField(
            model_name='goods',
            name='attach',
            field=models.ManyToManyField(related_name='attach_goods', to='goods.Attach', verbose_name='自定义信息'),
        ),
        migrations.AddField(
            model_name='goods',
            name='video',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='video', to='qfile.File', verbose_name='介绍视频'),
        ),
    ]