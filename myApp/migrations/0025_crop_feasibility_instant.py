# Generated by Django 2.2.14 on 2020-11-18 03:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0024_auto_20201006_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop_Feasibility_instant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feas_DRI_e', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_DRI')),
                ('feas_DRI_p', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_DRI_p')),
                ('feas_DRI_a', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_DRI_a')),
                ('feas_DRI_f', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_DRI_f')),
                ('feas_soc_acceptable', models.IntegerField(choices=[(3, 'no'), (2, 'maybe no'), (1, 'maybe yes'), (0, 'yes')], default=0, verbose_name='feas_social_wo')),
                ('feas_soc_acceptable_wo', models.IntegerField(choices=[(3, 'no'), (2, 'maybe no'), (1, 'maybe yes'), (0, 'yes')], default=0, verbose_name='feas_social_wo')),
                ('feas_soc_acceptable_c5', models.IntegerField(choices=[(3, 'no'), (2, 'maybe no'), (1, 'maybe yes'), (0, 'yes')], default=0, verbose_name='feas_social_c5')),
                ('feas_prod_skill', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_prod_skill')),
                ('feas_workload', models.IntegerField(choices=[(3, 'no'), (2, 'maybe no'), (1, 'maybe yes'), (0, 'yes')], default=0, verbose_name='feas_workload')),
                ('feas_tech_service', models.IntegerField(choices=[(1, 'no'), (2, 'maybe no'), (3, 'maybe yes'), (4, 'yes / there is no need for it since beneficiaries already have enough skill')], default=0, verbose_name='feas_tech_service')),
                ('feas_invest_fixed', models.IntegerField(choices=[(3, 'no'), (2, 'maybe no'), (1, 'maybe yes'), (0, 'yes')], default=0, verbose_name='feas_invest_fixed')),
                ('feas_invest_variable', models.IntegerField(choices=[(3, 'no'), (2, 'maybe no'), (1, 'maybe yes'), (0, 'yes')], default=0, verbose_name='feas_invest_variable')),
                ('feas_availability_non', models.IntegerField(choices=[(0, '10-12 mon'), (1, '7-9 mon'), (2, '4-6 mon'), (3, '0-3 mon')], default=0, verbose_name='feas_availability_non')),
                ('feas_availability_prod', models.IntegerField(choices=[(0, '0-3 mon'), (1, '4-6 mon'), (2, '7-9 mon'), (3, '10-12 mon')], default=0, verbose_name='feas_availability_prod')),
                ('feas_affordability', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_affordability')),
                ('feas_storability', models.IntegerField(choices=[(0, 'no'), (1, 'maybe no'), (2, 'maybe yes'), (3, 'yes')], default=0, verbose_name='feas_storability')),
                ('crop_score', models.IntegerField(default=0, verbose_name='crop_score')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='record_date')),
                ('created_by', models.CharField(default='', max_length=200, verbose_name='name')),
                ('myFCT', models.ForeignKey(default=436, on_delete=django.db.models.deletion.CASCADE, to='myApp.FCT', to_field='food_item_id')),
                ('myLocation', models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='myApp.Location')),
            ],
        ),
    ]
