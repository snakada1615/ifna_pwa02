# Generated by Django 2.2.11 on 2020-03-25 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0053_auto_20200325_0247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='AEZ_id',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='location',
            name='country',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
