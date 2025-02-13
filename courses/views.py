from django.shortcuts import render
from courses.models import CourseInfo

def home(request):
    classes = CourseInfo.objects.all()
    print("Courses:", list(classes))
    return render(request, 'home.html', {'classes' : classes})