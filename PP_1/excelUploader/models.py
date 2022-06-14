from django.db import models
from django import forms
class Employee(models.Model):
    employee_name = models.CharField(max_length=50)

    def __str__(self):
        return self.employee_name

    objects = models.Manager()

class ACS(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    company = models.CharField(max_length=50)
    datetime = models.DateTimeField()
    direction = models.CharField(max_length=5)
    door = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.employee_id

    objects = models.Manager()