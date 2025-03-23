from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=255) # Job title
    company = models.CharField(max_length=255) # Company name
    salary = models.CharField(max_length=100, null=True, blank=True)  # Salary might be missing
    region = models.CharField(max_length=255, null=True, blank=True)  # Renamed from 'location'
    description = models.TextField(null=True, blank=True)  # Description might be missing
    url = models.URLField(unique=True, null=True, blank=True)  # Allow NULL for existing jobs and ensure no duplicate job postings
    posted_date = models.CharField(max_length=50, null=True, blank=True)  # Date when job was posted

    def __str__(self):
        return self.title
