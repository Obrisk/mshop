# Generated by Django 2.0.7 on 2018-07-17 14:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wxapp', '0002_wxuser_qrcode_url'),
        ('account', '0002_auto_20180714_1025'),
    ]

    operations = [
        migrations.CreateModel(
            name='WxUserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asset', models.DecimalField(decimal_places=2, default=0, max_digits=30, verbose_name='佣金余额')),
                ('total_asset', models.DecimalField(decimal_places=2, default=0, max_digits=30, verbose_name='总计佣金')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='wxapp.WxUser')),
            ],
            options={
                'verbose_name': '用户账户',
                'verbose_name_plural': '用户账户',
            },
        ),
        migrations.RemoveField(
            model_name='orderinfo',
            name='goods',
        ),
        migrations.RemoveField(
            model_name='orderinfo',
            name='user',
        ),
        migrations.DeleteModel(
            name='WxUserAccountLog',
        ),
        migrations.DeleteModel(
            name='OrderInfo',
        ),
    ]
