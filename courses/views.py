from itertools import chain

from django.shortcuts import render
from django.db.models import Count
from numpy.ma.extras import unique

from courses.models import CourseInfo, CourseCatalog

def home(request):
    courses = CourseCatalog.objects.all()
    return render(request, 'home.html', {'courses' : courses})

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    offerings_subjects = offerings.values('semester', 'year', 'instructor', 'max_enrollment','students_enrolled').distinct()
    unique_offerings = offerings_subjects
    return render(request, 'course_page.html', {'offerings': unique_offerings})