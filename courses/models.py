from django.db import models
from django.db.models import Avg

# Create your models here.
class CourseInfo(models.Model):
    semester = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    course_number = models.IntegerField()
    course_title = models.CharField(max_length=255)
    catalog_title = models.CharField(max_length=255)
    f_credits = models.CharField(max_length=255)
    prereqs = models.CharField(max_length=255)
    meeting_pattern = models.CharField(max_length=255)
    meeting_time = models.CharField(max_length=255)
    instructor = models.CharField(max_length=255)
    max_enrollment = models.IntegerField()
    students_enrolled = models.IntegerField()
    primary_requests = models.IntegerField()
    major_requests = models.IntegerField()
    senior_requests = models.IntegerField()
    seniors_enrolled = models.IntegerField()
    junior_requests = models.IntegerField()
    juniors_enrolled = models.IntegerField()
    sophomore_requests = models.IntegerField()
    sophomores_enrolled = models.IntegerField()
    first_year_requests = models.IntegerField()
    first_years_enrolled = models.IntegerField()

class CourseCatalog(models.Model):
    subject = models.CharField(max_length=255)
    course_number = models.CharField(max_length=255)
    course_title = models.CharField(max_length=255)
    prereqs = models.CharField(max_length=255)