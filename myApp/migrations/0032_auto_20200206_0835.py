# Generated by Django 2.2.5 on 2020-02-06 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0031_auto_20200206_0830'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dri_aggr',
            old_name='nut_group',
            new_name='group',
        ),
    ]
