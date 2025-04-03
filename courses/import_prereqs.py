import csv
import os
import django

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "base.settings")
django.setup()

from courses.models import CourseCatalog


def import_csv_data(csv_file_path):
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create an instance of your model for each row
            my_model_instance = CourseCatalog(
                subject = row['subject'],
                course_number = row['course_number'],
                course_title = row['course_title'],
                prereqs = row['prerequisites'],
            )
            my_model_instance.save()


if __name__ == "__main__":
    csv_file_path = '/Users/tt/Desktop/prereqs.csv'
    import_csv_data(csv_file_path)
    print("CSV data has been loaded into the Django database.")