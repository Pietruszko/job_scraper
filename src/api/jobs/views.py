from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Job
from .serializers import JobSerializer

class JobViewSet(viewsets.ModelViewSet):

    queryset = Job.objects.all()
    serializer_class = JobSerializer

    # Enable filtering & searching
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Allow filtering by these fields
    filterset_fields = {
    'salary': ['exact'],
    'region': ['exact'],
    'company': ['exact'],
    'posted_date': ['exact', 'gte'],  # Allow filtering by "exact date" OR "greater than/equal"
}


    # Allow searching in these fields
    search_fields = ['title', 'description', 'company']

    # Allow ordering by salary, date posted
    ordering_fields = ['salary', 'posted_date']

def job_list_view(request):
    return render(request, "jobs_list.html")