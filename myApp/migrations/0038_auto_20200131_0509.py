# Generated by Django 2.2.5 on 2020-01-31 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0037_auto_20200131_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nut_group',
            field=models.CharField(choices=[('children under 5', 'children under 5'), ('pregnant woman', 'pregnant woman'), ('adlescent girl', 'adlescent girl'), ('adult', 'adult')], default='children under 5', max_length=200, verbose_name='nut_group'),
        ),
    ]
