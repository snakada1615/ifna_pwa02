# Generated by Django 2.2.5 on 2019-11-01 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0026_auto_20191101_0930'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='target_pop',
            field=models.IntegerField(default=0, verbose_name='target population'),
        ),
    ]
