# Generated by Django 2.2.5 on 2019-10-08 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0010_auto_20191002_2340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='crop',
            name='feas_availability',
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_DRI_a',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_DRI_a'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_DRI_f',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_DRI_f'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_DRI_p',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_DRI_p'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_affordability',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_affordability'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_availability_non',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_availability_non'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_availability_prod',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_availability_prod'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_soc_acceptable_c5',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_social_c5'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_soc_acceptable_wo',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_social_wo'),
        ),
        migrations.AddField(
            model_name='crop',
            name='feas_storability',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_storability'),
        ),
        migrations.AlterField(
            model_name='crop',
            name='feas_soc_acceptable',
            field=models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes')], default=1, verbose_name='feas_social_wo'),
        ),
    ]