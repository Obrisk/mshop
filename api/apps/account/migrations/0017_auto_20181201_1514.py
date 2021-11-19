# Generated by Django 2.1.2 on 2018-12-01 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_auto_20181123_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wxuseraccountlog',
            name='a_type',
            field=models.CharField(choices=[('asset', '分享返利'), ('bonus', '分销返佣'), ('use', '抵现'), ('use_return', '取消订单返还'), ('withdraw', '提现'), ('fail_withdraw_return', '提现失败返还'), ('recharge', '充值优惠')], max_length=32, verbose_name='类型'),
        ),
    ]
