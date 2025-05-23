# Generated by Django 4.2.19 on 2025-04-03 02:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0016_delete_coursecatalog"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseCatalog",
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
                ("subject", models.CharField(max_length=255)),
                ("course_number", models.CharField(max_length=255)),
                ("course_title", models.CharField(max_length=255)),
                ("prereqs", models.CharField(max_length=255)),
            ],
        ),
    ]
