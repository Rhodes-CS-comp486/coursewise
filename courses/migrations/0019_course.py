# Generated by Django 4.2.19 on 2025-04-03 20:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0018_merge_0012_initial_0017_coursecatalog"),
    ]

    operations = [
        migrations.CreateModel(
            name="Course",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
            ],
        ),
    ]
