# Generated by Django 2.2.5 on 2019-10-02 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0003_auto_20191001_2113'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='diet_type',
            field=models.IntegerField(choices=[(1, 'conventional'), (2, 'recommended')], default=1),
        ),
    ]
