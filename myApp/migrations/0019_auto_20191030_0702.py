# Generated by Django 2.2.5 on 2019-10-30 05:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myApp', '0018_auto_20191027_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='crop',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='record_date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='crop',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='family',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='person',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='crop',
            name='feas_availability_non',
            field=models.IntegerField(choices=[(0, '10-12 mon'), (1, '7-9 mon'), (2, '4-6 mon'), (3, '0-3 mon')], default=0, verbose_name='feas_availability_non'),
        ),
    ]