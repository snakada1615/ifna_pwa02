# Generated by Django 2.2.5 on 2019-10-02 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0008_auto_20191002_1801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='diet_type',
            field=models.IntegerField(choices=[(1, 'conventional'), (2, 'new crop')], default=1),
        ),
    ]