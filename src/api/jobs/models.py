from django.db import models

# Create your models here.

class Job(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    posted_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title