from django.shortcuts import render
from django.db.models import Sum, QuerySet, F, Avg, Value
from courses.models import CourseInfo, CourseCatalog
from django.db.models.functions import Greatest


def home(request):
    courses = CourseCatalog.objects.all()
    return render(request, 'home.html', {'courses' : courses})

def course_page(request, subject, number):
    offerings: QuerySet[CourseInfo] = CourseInfo.objects.filter(subject=subject.upper(), course_number=int(number))
    unique_offerings = offerings.values('semester', 'year', 'instructor').distinct()

    avg_class_size = offerings.aggregate(Avg("students_enrolled"))["students_enrolled__avg"] or 0

    #total_waitlist = offerings.aggregate(
        #total_waitlist=Sum(
           # (F('senior_requests') - F('seniors_enrolled')) +
           # (F('junior_requests') - F('juniors_enrolled')) +
           # (F('sophomore_requests') - F('sophomores_enrolled')) +
            #(F('first_year_requests') - F('first_years_enrolled'))))["total_waitlist"] or 0

    zero = Value(0)

    offerings = offerings.annotate(
        waitlist_size =(
        Greatest(F('senior_requests') - F('seniors_enrolled'), zero)+
        Greatest(F('junior_requests') - F('juniors_enrolled'), zero)+
        Greatest(F('sophomore_requests') - F('sophomores_enrolled'), zero)+
        Greatest(F('first_year_requests') - F('first_years_enrolled'), zero)
    ))

    waitlist_count = offerings.filter(waitlist_size__gt=0).count()
    total_offerings = offerings.count()
    has_waitlist = waitlist_count >= total_offerings / 2 if total_offerings > 0 else False


    return render(request, 'course_page.html', {
        'offerings': unique_offerings,
        'avg_class_size': avg_class_size,
        #'total_waitlist': total_waitlist,
        'has_waitlist': has_waitlist,
    })






