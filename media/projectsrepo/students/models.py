from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    DEPARTMENT = (
        ('COM', 'COM'),
        ('IT', 'IT'),
        ('ETS', 'ETS'),
        ('SIK', 'SIK'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    reg_no = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    department = models.CharField(max_length=200, choices=DEPARTMENT)


class Project(models.Model):
    LANGUAGE = (
        ('Java', 'Java'),
        ('Python', 'Python'),
        ('Javascript', 'Javascript'),
        ('PHP', 'PHP'),
        ('C', 'C'),
        ('C++', 'C++'),
        ('C#', 'C++'),
    )
    PROJECT_TYPE = (
        ('Web Application', 'Web Application'),
        ('Desktop', 'Desktop'),
        ('Artificial Intelligence', 'Artificial Intelligence'),
        ('Mobile Application', 'Mobile Appication'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    project_title = models.CharField(max_length=200)
    language = models.CharField(max_length=200, choices=LANGUAGE)
    project_type = models.CharField(max_length=200, choices=PROJECT_TYPE)
    project_concept = models.TextField()