# Generated by Django 2.2.5 on 2019-10-31 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0021_auto_20191031_0404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='fe',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='iron'),
        ),
        migrations.AlterField(
            model_name='person',
            name='vita',
            field=models.FloatField(blank=True, default=0, null=True, verbose_name='Vit-A'),
        ),
    ]
