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
                semester = row["Semester"],
                year = row["Year"],
                subject = row["Subject"],
                course_number = int(row["Course Number"]),
                course_title = row["Course Title"],
                instructor = row["Instructor"],
                max_enrollment = int(row["Max Enrollment"]),
                students_enrolled = int(row["Students Enrolled"]),
                primary_requests = int(row["Primary Requests"]),
                major_requests = int(row["Major Requests"]),
                senior_requests = int(row["Senior Requests"]),
                seniors_enrolled = int(row["Seniors Enrolled"]),
                junior_requests = int(row["Junior Requests"]),
                juniors_enrolled = int(row["Juniors Enrolled"]),
                sophomore_requests = int(row["Sophomore Requests"]),
                sophomores_enrolled = int(row["Sophomores Enrolled"]),
                first_year_requests = int(row["First-Year Requests"]),
                first_years_enrolled = int(row["First-Years Enrolled"]),
            )
            my_model_instance.save()


if __name__ == "__main__":
    csv_file_path = '/Users/tt/Desktop/compiled.csv'
    import_csv_data(csv_file_path)
    print("CSV data has been loaded into the Django database.")