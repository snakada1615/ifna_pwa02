# Generated by Django 2.2.11 on 2020-04-30 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0010_auto_20200428_0601'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop_individual',
            name='share_prod_buy',
            field=models.IntegerField(default=5, verbose_name='share_prod_buy'),
        ),
    ]