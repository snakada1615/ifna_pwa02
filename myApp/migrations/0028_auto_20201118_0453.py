# Generated by Django 2.2.14 on 2020-11-18 04:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0027_auto_20201118_0451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop_feasibility_instant',
            name='myLocation',
            field=models.ForeignKey(default=64, on_delete=django.db.models.deletion.CASCADE, to='myApp.Location'),
        ),
    ]
