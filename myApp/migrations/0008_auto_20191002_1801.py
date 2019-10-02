# Generated by Django 2.2.5 on 2019-10-02 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0007_auto_20191002_1757'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'verbose_name': 'Person informatin', 'verbose_name_plural': 'Person information'},
        ),
        migrations.AlterField(
            model_name='crop',
            name='food_wt_fe',
            field=models.FloatField(default=0, verbose_name='weight_Iron'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='food_wt_p',
            field=models.FloatField(default=0, verbose_name='weight_prot'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='food_wt_va',
            field=models.FloatField(default=0, verbose_name='weight_vitA'),
        ),
    ]
