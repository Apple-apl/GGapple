from django.db import models

class Employees(models.Model):
    name = models.CharField(max_length=100, null=False)
    surname = models.CharField(max_length=100, null=False)
    patronmic = models.CharField(max_length=120, null=True)
    age = models.IntegerField(null=False)
    date_of_birth = models.DateField(null=False)
    salary = models.FloatField(null=False)

