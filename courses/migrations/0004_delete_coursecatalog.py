# Generated by Django 4.2.19 on 2025-02-15 23:25

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0003_alter_coursecatalog_course_number"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CourseCatalog",
        ),
    ]
