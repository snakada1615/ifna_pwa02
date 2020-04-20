# Generated by Django 2.2.11 on 2020-04-20 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0005_delete_mystatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop_feasibility',
            name='myFCT',
            field=models.ForeignKey(default=436, on_delete=django.db.models.deletion.CASCADE, to='myApp.FCT', to_field='food_item_id'),
        ),
        migrations.AlterField(
            model_name='person',
            name='nut_group',
            field=models.CharField(choices=[('child 0-23 month', 'child 0-23 month'), ('child 24-59 month', 'child 24-59 month'), ('child 6-9 yr', 'child 6-9 yr'), ('adolescent boy', 'adolescent boy'), ('adolescent girl', 'adolescent girl'), ('adolescent pregnant', 'adolescent pregnant'), ('adult pregnant', 'adult pregnant'), ('adult', 'adult')], default='children 6 to 59 month', max_length=200, verbose_name='nut_group'),
        ),
    ]