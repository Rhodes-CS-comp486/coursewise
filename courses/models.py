from django.db import models
from django.db.models import Avg

# Create your models here.
class CourseInfo(models.Model):
    semester = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    course_number = models.IntegerField()
    course_title = models.CharField(max_length=255)
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

# Create your models here.
class CourseInfoEXT(models.Model):
    semester = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    course_number = models.IntegerField()
    instructor = models.CharField(max_length=255)
    f_credits = models.IntegerField()
    major_minor = models.IntegerField()
    capacity = models.IntegerField()
    total_enrollment = models.IntegerField()
    demand = models.CharField(max_length=255)

    class Meta:
        db_table = 'courses_courseinfoext'

    def __str__(self):
        return f"{self.subject} {self.course_number}"

class Course(models.Model):

    def _str_(self):
        return f"{self.subject} {self.course_number} - {self.course_title}"

class CourseCatalog(models.Model):
    subject = models.CharField(max_length=255)
    course_number = models.CharField(max_length=255)
    course_title = models.CharField(max_length=255)


