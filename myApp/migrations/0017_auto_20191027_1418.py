# Generated by Django 2.2.5 on 2019-10-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0016_auto_20191023_0450'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='m01_m',
            field=models.IntegerField(default=0, verbose_name='mon01_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m01_p',
            field=models.IntegerField(default=0, verbose_name='mon01_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m02_m',
            field=models.IntegerField(default=0, verbose_name='mon02_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m02_p',
            field=models.IntegerField(default=0, verbose_name='mon02_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m03_m',
            field=models.IntegerField(default=0, verbose_name='mon03_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m03_p',
            field=models.IntegerField(default=0, verbose_name='mon03_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m04_m',
            field=models.IntegerField(default=0, verbose_name='mon04_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m04_p',
            field=models.IntegerField(default=0, verbose_name='mon04_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m05_m',
            field=models.IntegerField(default=0, verbose_name='mon05_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m05_p',
            field=models.IntegerField(default=0, verbose_name='mon05_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m06_m',
            field=models.IntegerField(default=0, verbose_name='mon06_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m06_p',
            field=models.IntegerField(default=0, verbose_name='mon06_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m07_m',
            field=models.IntegerField(default=0, verbose_name='mon07_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m07_p',
            field=models.IntegerField(default=0, verbose_name='mon07_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m08_m',
            field=models.IntegerField(default=0, verbose_name='mon08_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m08_p',
            field=models.IntegerField(default=0, verbose_name='mon08_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m09_m',
            field=models.IntegerField(default=0, verbose_name='mon09_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m09_p',
            field=models.IntegerField(default=0, verbose_name='mon09_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m10_m',
            field=models.IntegerField(default=0, verbose_name='mon10_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m10_p',
            field=models.IntegerField(default=0, verbose_name='mon10_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m11_m',
            field=models.IntegerField(default=0, verbose_name='mon11_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m11_p',
            field=models.IntegerField(default=0, verbose_name='mon11_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m12_m',
            field=models.IntegerField(default=0, verbose_name='mon12_market'),
        ),
        migrations.AddField(
            model_name='crop',
            name='m12_p',
            field=models.IntegerField(default=0, verbose_name='mon12_prod'),
        ),
    ]
