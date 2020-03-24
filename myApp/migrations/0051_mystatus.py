# Generated by Django 2.2.11 on 2020-03-24 09:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myApp', '0050_community_crop_feasibility_crop_individual_crop_national_crop_subnational_dri_fct_person'),
    ]

    operations = [
        migrations.CreateModel(
            name='myStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crop_Community', models.IntegerField(blank=True, default=0)),
                ('crop_Individual', models.IntegerField(blank=True, default=0)),
                ('curr_User', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('myLocation', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='myApp.Community')),
            ],
        ),
    ]
