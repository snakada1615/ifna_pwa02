# Generated by Django 2.2.5 on 2019-10-31 02:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0020_auto_20191031_0402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='protein',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='protein'),
        ),
    ]
