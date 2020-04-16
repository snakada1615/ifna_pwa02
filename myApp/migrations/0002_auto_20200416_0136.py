# Generated by Django 2.2.11 on 2020-04-16 01:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='nut_group',
            field=models.CharField(choices=[('child 0-23 month', 'child 0-23 month'), ('child 24-59 month', 'child 24-59 month'), ('child 6-9 yr', 'child 6-9 yr'), ('adolescent boy', 'adolescent boy'), ('adolescent girl', 'adolescent girl'), ('pregnant women', 'pregnant women'), ('adult', 'adult')], default='children 6 to 59 month', max_length=200, verbose_name='nut_group'),
        ),
    ]
