# Generated by Django 4.1 on 2022-08-13 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('upstream_agenda_url', models.URLField(blank=True)),
                ('upstream_name', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('upstream_name', models.CharField(blank=True, max_length=200)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_control.event')),
            ],
        ),
        migrations.CreateModel(
            name='Performance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('upstream_uuid', models.UUIDField(blank=True)),
                ('planned_start', models.DateTimeField()),
                ('actual_start', models.DateTimeField(blank=True)),
                ('planned_duration', models.IntegerField()),
                ('actual_duration', models.IntegerField(blank=True)),
                ('start', models.IntegerField(choices=[(0, 'Manual'), (1, 'Auto Time'), (2, 'Auto Previous')], default=0)),
                ('end', models.IntegerField(choices=[(0, 'Manual'), (1, 'Auto Duration')], default=0)),
                ('venue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='production_control.venue')),
            ],
        ),
    ]
