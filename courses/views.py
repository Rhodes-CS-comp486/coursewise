from django.shortcuts import render
from django.db.models import Sum, QuerySet, F, Avg, Value
from courses.models import CourseInfo, CourseCatalog
from django.db.models.functions import Greatest
from django.shortcuts import render
from django.db.models import Avg, Count
from .models import CourseInfo


def home(request):
    courses = CourseCatalog.objects.all()
    return render(request, 'home.html', {'courses' : courses})

def course_page(request, subject, number):
    offerings = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor').distinct()

    avg_class_size = int(offerings.aggregate(Avg("students_enrolled"))["students_enrolled__avg"]) or 0


    return render(request, 'course_page.html', {
        'offerings': unique_offerings,
        'avg_class_size': avg_class_size,
    })

def instructor_history(request):
    # Get current semester info (you may want to adjust this logic)
    current_year = "2024"  # or get dynamically
    current_semester = "Spring"  # or get dynamically

    # Get all unique instructors
    instructors = CourseInfo.objects.values_list('instructor', flat=True).distinct()

    instructor_data = []

    for instructor in instructors:
        # Get current courses for this instructor
        current_courses = CourseInfo.objects.filter(
            instructor=instructor,
            year=current_year,
            semester=current_semester
        ).values('subject', 'course_number', 'course_title')

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

            # Calculate enrollment demand
            demand_level = _calculate_demand_level(history)

            # Determine typical schedule
            schedule = _determine_schedule(history)

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



