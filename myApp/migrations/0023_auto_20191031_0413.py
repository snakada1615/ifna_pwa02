# Generated by Django 2.2.5 on 2019-10-31 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0022_auto_20191031_0407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='fe',
            field=models.FloatField(default=0, verbose_name='iron'),
        ),
        migrations.AlterField(
            model_name='person',
            name='protein',
            field=models.FloatField(default=0, verbose_name='protein'),
        ),
        migrations.AlterField(
            model_name='person',
            name='vita',
            field=models.FloatField(default=0, verbose_name='Vit-A'),
        ),
    ]
