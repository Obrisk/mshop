# Generated by Django 2.1.2 on 2018-11-23 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20181122_1705'),
    ]

    operations = [
        migrations.AddField(
            model_name='wxuseraccountlog',
            name='balance',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=19, verbose_name='充值余额'),
        ),
        migrations.AlterField(
            model_name='wxuseraccountlog',
            name='a_type',
            field=models.CharField(choices=[('asset', '分销'), ('use', '抵现'), ('use_return', '取消订单返还'), ('withdraw', '提现'), ('fail_withdraw_return', '提现失败返还'), ('recharge', '充值优惠')], max_length=32, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='wxuseraccountlog',
            name='asset',
            field=models.DecimalField(decimal_places=2, max_digits=19, verbose_name='奖励收益'),
        ),
    ]
