# Generated by Django 2.2.11 on 2020-06-29 22:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0017_season'),
    ]

    operations = [
        migrations.AddField(
            model_name='season',
            name='myLocation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myApp.Location'),
        ),
    ]