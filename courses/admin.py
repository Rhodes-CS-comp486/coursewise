from django.contrib import admin
from courses.models import CourseInfo

# Register your models here.
@admin.register(CourseInfo)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('semester', 'year', 'subject', 'course_number','course_title', 'instructor', 'max_enrollment', 'students_enrolled', 'primary_requests', 'major_requests', 'senior_requests', 'seniors_enrolled', 'junior_requests', 'juniors_enrolled', 'sophomore_requests', 'sophomores_enrolled', 'first_year_requests', 'first_years_enrolled')
    list_filter = ('semester', 'year', 'subject', 'course_number','course_title', 'instructor')
    search_fields = ('semester', 'year', 'subject', 'course_number','course_title', 'instructor')


@admin.register(CourseInfo)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('subject', 'course_number','course_title', 'f_credits')
    list_filter = ('subject', 'course_number')
    search_fields = ('subject', 'course_number','course_title', 'f_credits')
