# Generated by Django 2.2.5 on 2020-02-02 09:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0046_auto_20200202_1245'),
    ]

    operations = [
        migrations.RenameField(
            model_name='crop',
            old_name='avail_farm',
            new_name='avail_type',
        ),
    ]
