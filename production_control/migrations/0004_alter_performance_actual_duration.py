# Generated by Django 4.1 on 2022-08-13 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production_control', '0003_alter_performance_actual_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='actual_duration',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
