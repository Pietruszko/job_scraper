import sys
import os

DJANGO_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../api"))
sys.path.append(DJANGO_PROJECT_PATH)
os.environ["DJANGO_SETTINGS_MODULE"] = "api.settings"
import django
django.setup()

from jobs.models import Job

def clear_jobs():
    print("🗑️ Clearing the Job table before scraping new data...")
    Job.objects.all().delete()  # ✅ Safe synchronous DB operation

if __name__ == "__main__":
    clear_jobs()
