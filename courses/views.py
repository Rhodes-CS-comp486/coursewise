from django.http import Http404
from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet, F, Avg, Value
from courses.models import CourseInfo, CourseCatalog, CourseInfoEXT
from django.db.models.functions import Greatest
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import CourseInfo
import datetime


def home(request):
    # Get the user's selected major and year from the session
    major = request.session.get('major', 'Not selected')
    year = request.session.get('year', 'Not selected')

    courses = CourseCatalog.objects.all()
    return render(request, 'home.html', {'major': major, 'year': year, 'courses': courses})

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor','max_enrollment', 'students_enrolled').distinct()

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

def instructor_history(request):
    # Get current semester info (you may want to adjust this logic)
    current_date = datetime.date.today()
    current_year = "2023"  # or get dynamically
    current_semester = "Spring"

    # Get all unique instructors
    instructors = CourseInfo.objects.values_list('instructor', flat=True).distinct()
    print(f"Instructors: {instructors}")

    instructor_data = []

    for instructor in instructors:
        # Get current courses for this instructor
        current_courses = CourseInfo.objects.filter(
            instructor=instructor,
            year=current_year,
            semester=current_semester
        ).values('subject', 'course_number', 'course_title')

        # print(f"Current courses for {instructor}: {current_courses}") #debug

        # Format current courses for display
        current_course_list = [
            f"{course['subject']} {course['course_number']}"
            for course in current_courses
        ]

        # Get historical data for each current course
        historical_courses = {}
        for course in current_courses:
            course_code = f"{course['subject']} {course['course_number']}"

            # Get all historical offerings of this course by this instructor
            history = CourseInfo.objects.filter(
                instructor=instructor,
                subject=course['subject'],
                course_number=course['course_number']
            ).order_by('-year', '-semester')

            # Calculate average class size
            avg_size = history.aggregate(
                avg_enrollment=Avg('students_enrolled')
            )['avg_enrollment']

            # print(f"Avg class size for {course_code}: {avg_size}")

            # Calculate enrollment demand
            demand_level = _calculate_demand_level(history)

            # print(f"Demand level for {course_code}: {demand_level}")

            # Determine typical schedule
            schedule = _determine_schedule(history)
            # print(f"Schedule for {course_code}: {schedule}")

            # Format semester list
            semesters = [f"{h.semester} {h.year}" for h in history]

            historical_courses[course_code] = {
                'course_title': course['course_title'],
                'semesters': semesters,
                'avg_class_size': round(avg_size) if avg_size else 0,
                'enrollment_demand': demand_level,
                'typical_schedule': schedule
            }

        instructor_data.append({
            'name': instructor,
            'current_courses': current_course_list,
            'historical_courses': historical_courses
        })

    #print(f"Instructor Data: {instructor_data}")

    return render(request, 'instructor_history.html', {
        'instructor_data': instructor_data
    })


def _calculate_demand_level(course_history):
    """Calculate demand level based on enrollment vs max capacity"""
    if not course_history:
        return "Unknown"

    # Calculate average fill rate
    total_fill_rate = 0
    count = 0
    for offering in course_history:
        if offering.max_enrollment > 0:  # Avoid division by zero
            fill_rate = (offering.students_enrolled / offering.max_enrollment) * 100
            total_fill_rate += fill_rate
            count += 1

    if count == 0:
        return "Unknown"

    avg_fill_rate = total_fill_rate / count

    if avg_fill_rate >= 90:
        return "High"
    elif avg_fill_rate >= 70:
        return "Medium"
    else:
        return "Low"


def _determine_schedule(course_history):
    """Determine typical schedule based on historical offerings"""
    semesters = set(offering.semester for offering in course_history)

    if 'Fall' in semesters and 'Spring' in semesters:
        return "Fall and Spring"
    elif 'Fall' in semesters:
        return "Fall only"
    elif 'Spring' in semesters:
        return "Spring only"
    else:
        return "Varies"

def demand_prediction(request, subject, course_number):
    # Start with an initial value
    initial_value = 10
    semester_filter = request.GET.get('semester', None)  # Optional, defaults to None
    f_credits_filter = request.GET.get('f_credits', None)  # Optional, defaults to None
    capacity_filter = request.GET.get('capacity', None)  # Optional, defaults to None

    # Build the initial query filtering by subject and course_number
    query_filter = {
        'subject': subject,
        'course_number': course_number,
    }

    # Add optional filters to the query if they are provided
    if semester_filter:
        query_filter['semester'] = semester_filter
    if f_credits_filter:
        query_filter['f_credits'] = f_credits_filter
    if capacity_filter:
        query_filter['capacity'] = capacity_filter

    # Query the CourseInfoEXT model using the dynamic query_filter
    course_info_ext = CourseInfoEXT.objects.filter(**query_filter)

    if not course_info_ext:
        raise Http404("Course not found in extended info.")


    for course_info in course_info_ext:






