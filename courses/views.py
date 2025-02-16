from django.shortcuts import render
from django.db.models import Count
from courses.models import CourseInfo, CourseCatalog

def home(request):
    courses = CourseCatalog.objects.all()
    return render(request, 'home.html', {'courses' : courses})

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor').distinct()
    return render(request, 'course_page.html', {'offerings' : unique_offerings})