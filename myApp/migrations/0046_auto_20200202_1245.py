# Generated by Django 2.2.5 on 2020-02-02 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0045_auto_20200202_1235'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='avail_market',
        ),
        migrations.RemoveField(
            model_name='crop',
            name='avail_new',
        ),
        migrations.AlterField(
            model_name='crop',
            name='avail_farm',
            field=models.IntegerField(default=1, verbose_name='available_farm'),
        ),
    ]
