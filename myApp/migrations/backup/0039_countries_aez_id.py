# Generated by Django 2.2.5 on 2020-02-16 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0038_auto_20200214_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='countries',
            name='AEZ_id',
            field=models.CharField(default='none', max_length=200),
        ),
    ]