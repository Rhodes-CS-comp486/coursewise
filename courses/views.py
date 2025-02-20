from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet, F, Avg, Value
from courses.models import CourseInfo, CourseCatalog
from django.db.models.functions import Greatest


def home(request):
    # Get the user's selected major and year from the session
    major = request.session.get('major', 'Not selected')
    year = request.session.get('year', 'Not selected')

    courses = CourseCatalog.objects.all()
    return render(request, 'home.html', {'major': major, 'year': year, 'courses': courses})

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor').distinct()

    avg_class_size = int(offerings.aggregate(Avg("students_enrolled"))["students_enrolled__avg"]) or 0


    return render(request, 'course_page.html', {
        'offerings': unique_offerings,
        'avg_class_size': avg_class_size,
    })
def startup(request):
    # Check if the form was submitted via POST
    if request.method == 'POST':
        major = request.POST.get('major')
        year = request.POST.get('year')

        # Check if both major and year are selected
        if major and year:
            # Save the selections to the session (so they can be accessed later)
            request.session['major'] = major
            request.session['year'] = year

            # Redirect the user to the home page
            return redirect('home')  # Redirect to the home page after form submission
        else:
            # If invalid, show an error message
            error_message = "Please select both a major and a year."
            return render(request, 'startup.html', {'error_message': error_message})

    # Default view for GET request (show the form)
    return render(request, 'startup.html')






