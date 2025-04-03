from collections import Counter

from django.http import Http404, HttpResponse, JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.db.models import Sum, QuerySet, F, Avg, Value, Max, F, ExpressionWrapper, FloatField
from courses.models import CourseInfo, CourseCatalog
from django.db.models.functions import Greatest
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import CourseInfo
from django.core.paginator import Paginator
import datetime
import json
from django.http import Http404, HttpResponse, JsonResponse

def home(request):
    f_credit = request.POST.get('f_credit', 'Not selected')
    major = request.session.get('major', 'Not selected')
    year = request.session.get('year', 'Not selected')

    # Get all courses
    if f_credit == 'Not selected':
        courses = CourseInfo.objects.values('subject', 'course_number').distinct().order_by('subject', 'course_number')
    else:
        courses = CourseInfo.objects.filter(f_credits__icontains=f_credit).values('subject', 'course_number').distinct().order_by('subject', 'course_number')

    favorites = request.session.get('favorites', [])
    favorite_courses = []

    # Get course details for each favorite
    for fav in favorites:
        subject, course_number = fav.split('-')
        course = CourseCatalog.objects.filter(subject=subject, course_number=course_number).first()
        if course:
            favorite_courses.append(course)

    # Allow user input for Search
    course_search = request.GET.get('courseSearch', '').strip()
    instructor_search = request.GET.get('instructorSearch', '').strip()

    # Apply filters based on search
    if course_search:
        # Split the search term by space
        search_parts = course_search.split()

        if len(search_parts) == 2:
            # Search format "Subject Number" (e.g., "AFS 105")
            subject = search_parts[0].upper()  # The first part is the subject
            number = search_parts[1]  # The second part is the course number
            return redirect('course_page', subject=subject, number=number)
        else:
            # If the search term does not follow the expected format (e.g., "AFS 105")
            return HttpResponse("Invalid course format. Please use 'Subject Number' format.", status=400)

    return render(request, 'home.html', {
        'major': major,
        'year': year,
        'course_search': course_search,
        'instructor_search': instructor_search,
        'courses': courses,
        'favorite_courses': favorite_courses
    })

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor', 'max_enrollment',
                                        'students_enrolled').distinct()

    catalog_pull = CourseCatalog.objects.filter(subject=subject.upper(), course_number=number).first()

    avg_class_size = int(offerings.aggregate(Avg("students_enrolled"))["students_enrolled__avg"]) or 0

    demand_data = demand_prediction(request, subject, number)

    suggestion_courses = demand_data.get('suggestion_courses', [])

    # Added Instructor information

    instructor_demand_data = []
    instructors = offerings.values_list('instructor', flat=True).distinct()

    for instructor in instructors:
        if instructor is not None:
            # Query all offerings of this course by this instructor
            history = offerings.filter(instructor=instructor)

            # Calculate average enrollment and capacity
            avg_data = history.aggregate(
                avg_enrollment=Avg('students_enrolled'),
                avg_capacity=Avg('max_enrollment')
            )
            avg_enrollment = avg_data['avg_enrollment'] or 0
            avg_capacity = avg_data['avg_capacity'] or 0

            # Get demand level using existing function
            demand_level = _calculate_demand_level(history)

            # Store instructor demand data
            instructor_demand_data.append({
                'instructor': instructor,
                'avg_enrollment': round(avg_enrollment),
                'avg_capacity': round(avg_capacity),
                'enrollment_vs_capacity': f"{round(avg_enrollment)}/{round(avg_capacity)}",
                'enrollment_demand': demand_level,
            })

    # Check if this course is in favorites
    favorites = request.session.get('favorites', [])
    is_favorite = f"{subject}-{number}" in favorites


    return render(request, 'course_page.html', {
        'offerings': unique_offerings,
        'avg_class_size': avg_class_size,
        'classification': demand_data["classification"],
        'demand_level': demand_data["demand_level"],
        'student_classification': demand_data["student_classification"],
        'student_major': demand_data["student_major"],
        'suggestion_courses': suggestion_courses,
        'instructor_demand_data': instructor_demand_data,
        'course': catalog_pull,
        'subject': subject,
        'course_number': number,
        'is_favorite': is_favorite
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
        'professor' : 0,
        'student_year' : 0,
        'major': 0,
        'past_demand': 0
        #'time_of_day' : 0,
        #'days_of_week' : 0
    }

    suggestion_courses = []  # Default empty

    course_number_int = int(course_number)

    if classification == "Low":
        # Determine course level range
        level_floor = (course_number_int // 100) * 100  # e.g., 300
        level_ceiling = level_floor + 100  # e.g., 400 (exclusive)

        suggestion_courses = CourseInfo.objects.filter(
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

def degree_requirements(request):
    # Majors and their Course Requirements
    majors = [
        {
            'id': 1,
            'name': 'Africana Studies',
            'courses': ['AFS 105', 'AFS 305', 'AFS 485', 'AFS Humanities/Fine Art Elective 1', 'AFS Humanities/Fine Art Elective 2', 'AFS Humanities/Fine Art Elective 3', 'AFS Humanities/Fine Art Elective 4', 'AFS Social/Natual Sciences 1', 'AFS Social/Natual Sciences 2', 'AFS Social/Natual Sciences 3', 'AFS Social/Natual Sciences 4']
        },
        {
            'id': 2,
            'name': 'Ancient Mediterranean Studies',
            'courses': ['AMS 275', 'AMS 474', 'AMS 475', 'AMS 476', 'AMS Concentration Elective 1', 'AMS Concentration Elective 2', 'AMS Concentration Elective 3', 'AMS Concentration Elective 4', 'AMS Concentration Elective 5', 'AMS Concentration Elective 6', 'AMS Concentration Elective 7', 'AMS Concentration Elective 8', 'AMS Concentration Elective 9']
        },
        {
            'id': 3,
            'name': 'Anthropology and Sociology',
            'courses': ['ANSO 103', 'ANSO 105', 'ANSO 351', 'ANSO Method Course', 'ANSO 380', 'ANSO 485', 'ANSO 486', 'ANSO Elective 1', 'ANSO Elective 2', 'ANSO Elective 3', 'ANSO Elective 4', 'ANSO Elective 5']
        },
        {
            'id': 4,
            'name': 'Art',
            'courses': ['Studio Art 1', 'Studio Art 2', 'ART 386', 'ART 485', 'ART 486', 'ART 152', 'ART Elective 1', 'ART Elective 2', 'ART Elective 3', 'ART Elective 4']
        },
        {
            'id': 5,
            'name': 'Art History',
            'courses': ['Studio Art', 'ART 151', 'ART 152', 'ART 218', 'ART 223', 'ART 242', 'ART 475', 'ART HIST Elective 1', 'ART HIST Elective 2', 'ART HIST Elective 3']
        },
        {
            'id': 6,
            'name': 'Art and Art History',
            'courses': ['Studio Art 1', 'Studio Art 2', 'Studio Art 3', 'ART 386', 'ART 485', 'ART 486', 'ART 475', 'ART 151', 'ART 152', 'ART 218', 'ART 223', 'ART 242', 'ART Elective 1', 'ART Elective 2']
        },
        {
            'id': 7,
            'name': 'Biochemistry and Molecular Biology',
            'courses': ['CHEM 120/125L', 'CHEM 211', 'CHEM 212/212L', 'CHEM 240/240L', 'BIOL 130/131L', 'BIOL 140/141L', 'BIOL 307', 'BIOL 325/325L', 'CHEM 315', 'BMB 310', 'BMB 485/486', 'MATH Elective', 'BMB Elective w/ Lab', 'BMB Elective']
        },
        {
            'id': 8,
            'name': 'Biology',
            'courses': ['BIOL 130/131L', 'BIOL 140/141L', 'CHEM 120/125L', 'CHEM 211', 'Statistics Course', 'Computational Course', 'BIOL 485/486', 'BIOL Concentration Elective 1', 'BIOL Concentration Elective 2', 'BIOL Concentration Elective 3', 'BIOL Concentration Elective 4', 'BIOL Concentration Elective 5', 'BIOL Concentration Elective 6']
        },
        {
            'id': 9,
            'name': 'Biomathematics',
            'courses': ['MATH 122', 'MATH 211', 'COMP 141', 'MATH 214', 'MATH 315', 'BIOL 130/131L', 'BIOL 140/141L', 'BIOL 300 Elective', 'MATH Elective 1', 'MATH Elective 2', 'BIOL Elective 1 w/ Lab', 'BIOL Elective 2 w/ Lab', 'BIOL Elective 3', 'Senior Research']
        },
        {
            'id': 10,
            'name': 'Business',
            'courses': ['BUS 241', 'BUS 243', 'BUS 351', 'BUS 361', 'BUS 371', 'BUS 486', 'ECON 100', 'Statistics Course', 'Calculus Course', 'Business Elective 1', 'Business Elective 2', 'Business Elective 3']
        },
        {
            'id': 11,
            'name': 'Chemistry',
            'courses': ['CHEM 120/125L', 'CHEM 211', 'CHEM 212/212L', 'CHEM 240/240L', 'CHEM 311/312L', 'CHEM Elective 1', 'CHEM Elective 2', 'CHEM Elective 3', 'Physics 1', 'Physics 2', 'MATH 122', 'CHEM 486']
        },
        {
            'id': 12,
            'name': 'Chinese Studies',
            'courses': ['CHIN 202', 'CHIN 301', 'CHIN 302', 'CHIN Elective 1', 'CHIN Elective 2', 'CHIN Elective 3', 'HIST Elective 1', 'HIST Elective 2', 'CHIN 485']
        },
        {
            'id': 13,
            'name': 'Computer Science',
            'courses': ['COMP 141', 'COMP 142', 'COMP 172', 'COMP 231', 'COMP 241', 'COMP 251', 'COMP 485', 'COMP 486', 'MATH Elective', 'Theory Course', 'Systems Course', 'Applications Course', 'COMP Elective 1', 'COMP Elective 2']
        },
        {
            'id': 14,
            'name': 'Data Analytics',
            'courses': ['COMP 141', 'DATA 242', 'DATA/MATH 244', 'DATA/COMP/MATH 344', 'Statistics Course', 'MATH 212 OR ECON 420', 'DATA 486', 'Ethics Course', 'DATA Elective 1', 'DATA Elective 2', 'Concentration Elective']
        },
        {
            'id': 15,
            'name': 'Economics',
            'courses': ['ECON 100', 'ECON 201', 'ECON 202', 'ECON 290', 'ECON 420', 'ECON 486', 'Math Elective', 'ECON Elective 1', 'ECON Elective 2', 'ECON Elective 3', 'ECON Elective 4', 'ECON Elective 5']
        },
        {
            'id': 16,
            'name': 'Economics and Business',
            'courses': ['ECON 100', 'ECON 201', 'ECON 202', 'ECON 290', 'ECON 420', 'ECON 486', 'BUS 241', 'BUS 243', 'BUS 351', 'BUS 361', 'BUS 371', 'BUS 486', 'ECON Elective 1', 'ECON Elective 2', 'ECON Elective 3', 'ECON Elective 4', 'BUS Elective 1', 'BUS Elective 2']
        },
        {
            'id': 17,
            'name': 'Economics and International Studies',
            'courses': ['ECON 100', 'ECON 201', 'ECON 202', 'ECON 290', 'ECON 310', 'ECON 312', 'ECON 486 OR INTS 485', 'ECON 407 OR 420', 'INTS 110', 'INTS 120', 'INTS 201', 'INTS Elective 1', 'INTS Elective 2', 'INTS Elective 3', 'MATH Elective', 'Language Elective']
        },
        {
            'id': 18,
            'name': 'Educational Studies',
            'courses': ['EDUC 201', 'EDUC 222', 'PPE Elective 1', 'PPE Elective 2', 'EDUC 485', 'EDUC Track Elective 1', 'EDUC Track Elective 2', 'EDUC Track Elective 3', 'EDUC Track Elective 4', 'EDUC Track Elective 5', 'EDUC Track Elective 6', 'OPT: Licensure Reqs']
        },
        {
            'id': 19,
            'name': 'English',
            'courses': ['ENGL 285', 'ENGL 485', 'ENGL Concentration Elective 1', 'ENGL Concentration Elective 2', 'ENGL Concentration Elective 3', 'ENGL Concentration Elective 4', 'ENGL Concentration Elective 5', 'ENGL Concentration Elective 6', 'ENGL Concentration Elective 7', 'ENGL Concentration Elective 8', 'ENGL Concentration Elective 9']
        },
        {
            'id': 20,
            'name': 'Environmental Sciences',
            'courses': ['ENVS 150', 'ENVS Intro Course 1', 'ENVS Intro Course 2', 'ENVS Intro Course 3', 'Statistics Course', 'ENVS Elective 1 w/ Lab', 'ENVS Elective 2 w/ Lab', 'ENVS Elective 3 w/ Lab', 'ENVS Elective 4', 'ENVS Elective 5', 'ENVS Elective 6', 'ENVS 225', 'ENVS 486', 'Experiential Learning']
        },
        {
            'id': 21,
            'name': 'Environmental Studies',
            'courses': ['ENVS 150', 'ENVS Intro Course', 'ECON 100', 'ENVS Elective 1', 'ENVS Elective 2', 'ENVS Elective 3', 'ENVS Elective 4', 'ENVS Elective 5', 'ENVS Elective 6', 'ENVS Elective 7', 'ENVS Elective 8', 'ENVS 225', 'ENVS 486', 'Experiential Learning']
        },
        {
            'id': 22,
            'name': 'French and Francophone Studies',
            'courses': ['FREN 201', 'FREN 202', 'FREN 301', 'FREN 486', 'FREN 320 OR 321 OR 322', 'FREN 323 OR 324 OR 325', 'FREN Elective 1', 'FREN Elective 2', 'FREN Elective 3', 'FREN Elective 4']
        },
        {
            'id': 23,
            'name': 'German Studies',
            'courses': ['GRST Placement Course', 'GRST 301', 'GRST 302', 'GRST 486', 'GRST Concentration Elective 1', 'GRST Concentration Elective 2', 'GRST Concentration Elective 3', 'GRST Concentration Elective 4', 'GRST Concentration Elective 5']
        },
        {
            'id': 24,
            'name': 'Health Equity',
            'courses': ['URBN 201', 'Policy Elective', 'HLEQ Elective 1', 'HLEQ Elective 2','HLEQ Elecive 3', 'HLEQ Elective 4', 'HLEQ Elective 5', 'HLEQ Elective 6', 'Methods Elective', 'Community Engagement Elective', 'URBN 385', 'URBN 485']
        },
        {
            'id': 25,
            'name': 'History',
            'courses': ['HIST 485', 'HIST Elective 1', 'HIST Elective 2', 'HIST Elective 3', 'HIST Elective 4', 'HIST Elective 5', 'HIST Elective 6', 'HIST Elective 7', 'HIST Elective 8', 'HIST Elective 9', 'HIST Elective 10']
        },
        {
            'id': 26,
            'name': 'History and International Studies',
            'courses': ['HIST 300', 'HIST Elective 1', 'HIST Elective 2', 'INTS 110', 'INTS 120', 'INTS 201', 'INTS 301', 'ECON 100', 'INTS Studies Elective 1', 'HIST Elective 3', 'HIST or INTS Elective', 'INTS 485', 'Language Elective']
        },
        {
            'id': 27,
            'name': 'International Studies',
            'courses': ['INTS 110', 'INTS 120', 'INTS 201', 'INTS 301', 'INTS 485', 'ECON 100 OR INTS 311', 'INTS  Global Leadership Elective 1', 'INTS Global Leadership Elective 2', 'INTS Regional Leadership Elective 1', 'INTS Regional Leadership Elective 2', 'INTS Elective', 'Language Elective', 'International Experience']
        },
        {
            'id': 28,
            'name': 'Latin American and Latinx Studies',
            'courses': ['LALS 200', 'LALS 485', 'LALS Elective 1', 'LALS Elective 2', 'LALS Elective 3', 'LALS Elective 4', 'LALS Elective 5', 'LALS Elective 6', 'LALS Elective 7', 'LALS Elective 8', 'LALS Elective 9']
        },
        {
            'id': 29,
            'name': 'Mathematics',
            'courses': ['MATH 122', 'MATH 201', 'MATH 223', 'MATH 261', 'MATH 386', 'MATH 485 AND/OR 486', 'Statics Elective', 'Modeling Elective', 'Proof Elective', 'MATH Elective 1', 'MATH Elective 2', 'MATH Elective 3', 'MATH Elective 4']
        },
        {
            'id': 30,
            'name': 'Mathematics and Economics',
            'courses': ['ECON 100', 'ECON 201', 'ECON 202', 'ECON 290', 'ECON 407', 'ECON 420', 'ECON Elective', 'MATH 122', 'MATH 201', 'MATH 223', 'MATH 251', 'MATH 261', 'MATH 311 OR 321', 'ECON OR MATH Senior Seminar']
        },
        {
            'id': 31,
            'name': 'Media Studies',
            'courses': ['MST 202 OR ART 102', 'MST 385', 'MST 485', 'MST Concentration Elective 1', 'MST Concentration Elective 2', 'MST Concentration Elective 3', 'MST Concentration Elective 4', 'MST Elective 5', 'MST Elective 6', 'MST Elective 7']
        },
        {
            'id': 32,
            'name': 'Music',
            'courses': ['MUSC 204', 'MUSC Theory 1', 'MUSC Theory 2', 'MUSC 227', 'MUSC 228', 'F9 Elective', 'Applied Lessons', 'Large Ensemble', 'MUSC 485/486', 'MUSC 414', 'MUSC 415 OR Composition', 'MUSC Elective 1', 'MUSC Elective 2']
        },
        {
            'id': 33,
            'name': 'Music and Psychology',
            'courses': ['MUSC 204', 'MUSC Theory 1', 'MUSC Theory 2', 'History & Literature Elective', 'Large Ensemble Performance', 'Applied Lessons', 'MUSC Elective 1', 'MUSC Elective 2', 'PSYC 150', 'PSYC 200', 'PSYC 211', 'PSYC 216', 'Advanced Research Methods', 'PSYC Concentration Elective 1', 'PSYC Concentration Elective 2', 'Senior Experience']
        },
        {
            'id': 34,
            'name': 'Neuroscience',
            'courses': ['CHEM 120/125L', 'BIOL 130/131L', 'BIOL 140/141L', 'PSYC 150', 'PSYC OR MATH 211', 'NEUR 270', 'NEUR 485 OR 486', 'Depth 1', 'Depth 2', 'Breadth 1', 'Breadth 2', 'NEUR Elective 1', 'NEUR Elective 2']
        },
        {
            'id': 35,
            'name': 'Philosophy',
            'courses': ['PHIL 200', 'PHIL 222', 'PHIL 486', 'Knowledge and Reasoning Elective', 'Social Philosophy Elective', 'History of Philosophy Elective', 'PHIL Elective 1', 'PHIL Elective 2', 'PHIL Elective 3', 'PHIL Elective 4', 'PHIL Elective 5']
        },
        {
            'id': 36,
            'name': 'Philosophy Politics and Economics',
            'courses': ['PPE 110', 'ECON 100', 'ECON 201 OR 202', 'ECON 323', 'INTS 310 OR 311', 'PHIL 225', 'PHIL 345', 'Research Methods', 'PPE 486', 'PPE Elective 1', 'PPE Elective 2', 'PPE Elective 3']
        },
        {
            'id': 37,
            'name': 'Physics',
            'courses': ['PHYS 111', 'PHYS 112', 'PHYS 113', 'PHYS 114', 'PHYS 211', 'PHYS 213', 'PHYS 250', 'PHYS 301', 'PHYS 305', 'PHYS 401', 'PHYS 406', 'PHYS 486', 'PHYS Elective 1', 'PHYS Elective 2', 'MATH 122', 'MATH 223']
        },
        {
            'id': 38,
            'name': 'Political Science',
            'courses': ['PLAW 151', 'PLAW 270', 'PLAW 485', 'Political Thought and Philosophy Elective', 'INTS 110 or 120', 'PLAW Elective 1', 'PLAW Elective 2', 'PLAW Elective 3', 'PLAW Elective 4', 'PLAW Elective 5', 'PLAW Elective 6']
        },
        {
            'id': 39,
            'name': 'Political Science and International Studies',
            'courses': ['INTS 110', 'INTS 120', 'INTS 201', 'INTS Elective 1', 'INTS Elective 2', 'INTS Elective 3', 'PLAW 151', 'PLAW 340 OR 360', 'American Politics Elective', 'Political Theory Elective', 'PLAW Elective', 'ECON 100 OR INTS 311', 'INTS 301 OR PLAW 270', 'INTS OR PLAW 485', 'Language Elective']
        },
        {
            'id': 40,
            'name': 'Psychology',
            'courses': ['PSYC 150', 'PSYC 200', 'PSYC 211', 'Development Elective', 'Cognition and Learning Elective', 'Biological Bases of Behavior Elective', 'Sociocultural Behavior Elective', 'Health and Well-Being Elective', 'Advanced Methods', 'Community Based Elective', 'PSYC Elective', 'PSYC 485']
        },
        {
            'id': 41,
            'name': 'Religious Studies',
            'courses': ['RELS 255', 'RELS 256', 'RELS 251 OR 253 OR 258', 'Bible Elective', 'Theology and Ethics Elective', 'RELS Elective 1', 'RELS Elective 2', 'RELS Elective 3', 'RELS 485']
        },
        {
            'id': 42,
            'name': 'Russian Studies',
            'courses': ['RUSS 202', 'RUSS 205', 'RUSS 212 OR 300', 'RUSS Advanced Elective 1', 'Russ Advanced Elective 2', 'RUSS 410', 'RUSS 486', 'RUSS 285', 'ML 280']
        },
        {
            'id': 43,
            'name': 'Russian and International Studies',
            'courses': ['RUSS 201', 'RUSS 202', 'RUSS 301', 'RUSS 302', 'RUSS Elective', 'INTS 110', 'INTS 120', 'INTS 201', 'INTS 301', 'INTS Global Leadership Elective', 'INTS Regional Leadership Elective', 'ECON 100 OR INTS 311', 'INTS 485']
        },
        {
            'id': 44,
            'name': 'Spanish Studies',
            'courses': ['SPAN 301 OR 302', 'SPAN 303', 'SPAN 306', 'SPAN 486', 'SPAN Elective 1', 'SPAN Elective 2', 'SPAN Elective 3', 'SPAN Elective 4', 'SPAN Elective 5']
        },
        {
            'id': 45,
            'name': 'Urban Studies',
            'courses': ['URBN 201', 'PLAW 206', 'Race and Ethnicity Elective', 'Methods Course', 'Community Engagement Elective', 'URBN 385', 'URBN 485', 'URBN Elective 1', 'URBN Elective 2', 'URBN Elective 3', 'URBN Elective 4']
        },
    ]

    # Get the search query
    search_query = request.GET.get('search_query', '').lower()

    # Filter the majors based on the search query
    if search_query:
        majors = [major for major in majors if search_query in major['name'].lower()]

    # Get the major selected by the user
    major_id = request.GET.get('major_id')
    major = None
    courses = []
    if major_id:
        major = next((m for m in majors if str(m['id']) == major_id), None)
        if major:
            courses = major['courses']

    # Track completed courses in the session
    if 'completed_courses' not in request.session:
        request.session['completed_courses'] = []

    completed_courses = request.session['completed_courses']

    # Calculate progress
    total_courses = len(courses)
    completed_count = len([course for course in courses if course in completed_courses])
    progress_percentage = (completed_count / total_courses) * 100 if total_courses > 0 else 0


    return render(request, 'degree_requirements.html', {
            'majors': majors,
            'search_query': search_query,
            'major': major,
            'courses': courses,
            'completed_courses': completed_courses,
            'progress_percentage': progress_percentage,
        })

def update_progress(request):
    completed_courses = []
    for course_key in request.POST:
        if course_key.startswith('course_'):
            course_name = course_key.split('_')[1]
            completed_courses.append(course_name)

        # Save the updated course progress to the session
        request.session['completed_courses'] = completed_courses

    # Redirect back to the degree requirements page
    return HttpResponseRedirect(reverse('degree_requirements'))


def add_to_favorites(request, subject, course_number):
    if 'favorites' not in request.session:
        request.session['favorites'] = []

    course_id = f"{subject}-{course_number}"
    favorites = request.session['favorites']

    if course_id not in favorites:
        favorites.append(course_id)
        request.session['favorites'] = favorites
        request.session.modified = True

    return JsonResponse({'status': 'success'})


def remove_from_favorites(request, subject, course_number):
    if 'favorites' in request.session:
        course_id = f"{subject}-{course_number}"
        favorites = request.session['favorites']

        if course_id in favorites:
            favorites.remove(course_id)
            request.session['favorites'] = favorites
            request.session.modified = True

    return JsonResponse({'status': 'success'})

