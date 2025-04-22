import csv
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from courses.models import CourseInfo


def import_csv_data(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create an instance of your model for each row
            my_model_instance = CourseInfo(
                semester = row['Semester'],
                year = row['Year'],
                subject = row['Subject'],
                course_number = row['Course Number'],
                course_title = row['Course Title'],
                catalog_title = row['Catalog Title'],
                f_credits = row['F-Credits'],
                prereqs = row['Prerequisites'],
                meeting_pattern = row['Meeting Pattern'],
                meeting_time = row['Meeting Time'],
                instructor = row['Instructor'],
                max_enrollment = row['Max Enrollment'],
                students_enrolled = row['Students Enrolled'],
                primary_requests = row['Primary Requests'],
                major_requests = row['Major Requests'],
                senior_requests = row['Senior Requests'],
                seniors_enrolled = row['Seniors Enrolled'],
                junior_requests = row['Junior Requests'],
                juniors_enrolled = row['Juniors Enrolled'],
                sophomore_requests = row['Sophomore Requests'],
                sophomores_enrolled = row['Sophomores Enrolled'],
                first_year_requests = row['First-Year Requests'],
                first_years_enrolled = row['First-Years Enrolled'],
            )
            my_model_instance.save()


if __name__ == "__main__":
    csv_file_path = '/Users/tt/Desktop/complete.csv'
    import_csv_data(csv_file_path)
    print("CSV data has been loaded into the Django database.")