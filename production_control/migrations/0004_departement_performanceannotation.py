# Generated by Django 4.1 on 2023-05-18 09:14

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("production_control", "0003_event_time_offset"),
    ]

    operations = [
        migrations.CreateModel(
            name="Departement",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("default_annotation", models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name="PerformanceAnnotation",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("content", models.TextField()),
                (
                    "departement",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="production_control.departement",
                    ),
                ),
                (
                    "performance",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="production_control.performance",
                    ),
                ),
            ],
        ),
    ]
