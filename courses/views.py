from collections import Counter

from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet, F, Avg, Value, Max, F, ExpressionWrapper, FloatField
from courses.models import CourseInfo, CourseCatalog, CourseInfoEXT
from django.db.models.functions import Greatest
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import CourseInfo, CourseInfoEXT
from django.core.paginator import Paginator
import datetime
import json

def home(request):
    major = request.session.get('major', 'Not selected')
    year = request.session.get('year', 'Not selected')

    if request.method == 'POST':
    # Get the user's selected major and year from the session
        major = request.session.get('major', 'Not selected')
        year = request.session.get('year', 'Not selected')

        request.session['major'] = major
        request.session['year'] = year

    courses = CourseCatalog.objects.all()

    return render(request, 'home.html', {'major': major, 'year': year, 'courses': courses})

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor','max_enrollment', 'students_enrolled').distinct()

    avg_class_size = int(offerings.aggregate(Avg("students_enrolled"))["students_enrolled__avg"]) or 0

    demand_data = demand_prediction(request, subject, number)

    suggestion_courses = demand_data.get('suggestion_courses', [])


    return render(request, 'course_page.html', {
        'offerings': unique_offerings,
        'avg_class_size': avg_class_size,
        'classification': demand_data["classification"],
        'demand_level': demand_data["demand_level"],
        'student_classification': demand_data["student_classification"],
        'student_major': demand_data["student_major"],
        'suggestion_courses': suggestion_courses
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
    instances = CourseInfo.objects.filter(subject=subject, course_number=course_number).distinct()
    student_major = request.session.get('major')
    student_year = request.session.get('year')
    class_enrollment = 0
    course_demand = 0
    prediction_offerings = instances.count()
    demand_offerings = instances.count()

    for instance in instances:
        all_requests = instance.senior_requests + instance.junior_requests + instance.sophomore_requests + instance.first_year_requests

        if instance.max_enrollment == 0:
            demand_offerings = demand_offerings - 1
            continue

        instance_demand = all_requests / instance.max_enrollment
        course_demand = course_demand + instance_demand

        if student_year == "Freshman":
            class_requests = instance.first_year_requests
            class_enrolled = instance.first_years_enrolled
        elif student_year == "Sophomore":
            class_requests = instance.sophomore_requests
            class_enrolled = instance.sophomores_enrolled
        elif student_year == "Junior":
            class_requests = instance.junior_requests
            class_enrolled = instance.juniors_enrolled
        else:
            class_requests = instance.senior_requests
            class_enrolled = instance.seniors_enrolled

        if class_requests == 0:
            prediction_offerings = prediction_offerings - 1
            continue

        instance_class_demand = class_enrolled / class_requests
        class_enrollment = class_enrollment + instance_class_demand


    if demand_offerings > 0:
        demand_num = course_demand / demand_offerings
    else:
        demand_num = 0
    if prediction_offerings > 0:
        prediction_num = class_enrollment / prediction_offerings
    else:
        prediction_num = 0

    if prediction_num > 0.7:
        classification = 'High'
    elif 0.4 < prediction_num <= 0.7:
        classification = 'Medium'
    else:
        classification = 'Low'

    if demand_num > 0.7:
        demand_level = 'High'
    elif 0.4 < demand_num <= 0.7:
        demand_level = 'Medium'
    else:
        demand_level = 'Low'

    impact_factors = {
        'professor': 0,
        'student_year': 0,
        'time_of_day': 0,
        'days_of_week': 0
    }

    suggestion_courses = []  # Default empty

    course_number_int = int(course_number)

    if classification == "Low":
        # Determine course level range
        level_floor = (course_number_int // 100) * 100  # e.g., 300
        level_ceiling = level_floor + 100  # e.g., 400 (exclusive)

        suggestion_courses = CourseInfoEXT.objects.filter(
            subject=subject,
            course_number__gte=level_floor,
            course_number__lt=level_ceiling
        ).exclude(course_number=course_number_int).values('subject', 'course_number').distinct()

    print("Suggestions:", suggestion_courses)

    return {
        "classification": classification,
        "demand_level": demand_level,
        "impact_factors": impact_factors,
        "student_classification": student_year,
        "student_major": student_major,
        "suggestion_courses": suggestion_courses,
    }

def historical_pattern_analysis(request):
    # Get data for courses from the past 2 years
    courses = CourseInfo.objects.all().order_by('-year', '-semester')

    # Get unique semesters for the last 2 years (assuming data exists)
    recent_semesters = list(courses.values_list('semester', 'year').distinct())[:4]  # Last 2 years (4 semesters)

    # Prepare data structure for the template
    enrollment_data = {
        'semesters': [],
        'fill_rates': [],
        'waitlist_data': [],
        'enrollment_speed': []
    }

    for semester, year in recent_semesters:
        semester_display = f"{semester} {year}"
        enrollment_data['semesters'].append(semester_display)

        # Get courses for this semester
        semester_courses = courses.filter(semester=semester, year=year)

        # Calculate fill rate (students enrolled / max enrollment)
        fill_rate = semester_courses.annotate(
            fill_rate=ExpressionWrapper(
                F('students_enrolled') * 100.0 / F('max_enrollment'),
                output_field=FloatField()
            )
        ).aggregate(avg_fill_rate=Avg('fill_rate'))['avg_fill_rate'] or 0

        enrollment_data['fill_rates'].append(round(fill_rate, 1))

        # Calculate waitlist data (approximation using requests vs. enrolled)
        total_requests = semester_courses.aggregate(
            total=Avg(F('primary_requests') + F('major_requests') +
                      F('senior_requests') + F('junior_requests') +
                      F('sophomore_requests') + F('first_year_requests'))
        )['total'] or 0

        total_enrolled = semester_courses.aggregate(
            total=Avg('students_enrolled')
        )['total'] or 0

        # Estimated waitlist length (requests - enrolled)
        waitlist_estimate = max(0, total_requests - total_enrolled)
        enrollment_data['waitlist_data'].append(round(waitlist_estimate, 1))

        # Enrollment speed approximation (percentage of requests fulfilled)
        if total_requests > 0:
            fulfillment_rate = (total_enrolled / total_requests) * 100
        else:
            fulfillment_rate = 100

        # Invert fulfillment rate to represent speed (higher = faster fill)
        speed_metric = 100 - fulfillment_rate if fulfillment_rate < 100 else 0
        enrollment_data['enrollment_speed'].append(round(speed_metric, 1))

    # Reverse the data to have chronological order
    for key in enrollment_data:
        enrollment_data[key].reverse()

    # Convert to JSON for JavaScript
    enrollment_json = json.dumps(enrollment_data)

    # Get top 5 highest demand courses
    high_demand_courses = courses.annotate(
        demand_ratio=ExpressionWrapper(
            F('students_enrolled') * 100.0 / F('max_enrollment'),
            output_field=FloatField()
        )
    ).order_by('-demand_ratio')[:5]

    return render(request, 'historical_pattern_analysis.html', {
        'enrollment_data': enrollment_json,
        'high_demand_courses': high_demand_courses,
    })