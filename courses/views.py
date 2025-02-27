from django.shortcuts import render
from django.db.models import Avg, Max, F, ExpressionWrapper, FloatField
from .models import CourseInfo
import json


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

    return render(request, 'courses/historical_pattern_analysis.html', {
        'enrollment_data': enrollment_json,
        'high_demand_courses': high_demand_courses,
    })



