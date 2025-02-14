from django.shortcuts import render
from courses.models import CourseInfo

def home(request):
    courses = CourseInfo.objects.all()
    return render(request, 'home.html', {'courses' : courses})