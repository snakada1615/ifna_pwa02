# Generated by Django 2.2.11 on 2020-04-06 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0066_auto_20200406_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop_individual',
            name='id_table',
            field=models.IntegerField(default=0),
        ),
    ]
