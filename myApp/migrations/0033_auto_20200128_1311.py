# Generated by Django 2.2.5 on 2020-01-28 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0032_crop_aez_crop_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop_region',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='record_date'),
        ),
    ]
