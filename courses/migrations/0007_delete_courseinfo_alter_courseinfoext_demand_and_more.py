# Generated by Django 4.2.19 on 2025-03-19 23:52

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("courses", "0006_course_courseinfoext"),
    ]

    operations = [
        migrations.DeleteModel(
            name="CourseInfo",
        ),
        migrations.AlterField(
            model_name="courseinfoext",
            name="demand",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterModelTable(
            name="courseinfoext",
            table="courses_courseinfoext",
        ),
    ]
