from django.db import models

# Create your models here.
#table case 
class Case(models.Model):
    case_id = models.CharField(max_length=100)
    date_creation = models.DateField(null=True, blank=True)
    edit_date = models.DateField(null=True, blank=True)
    edited_by_employee = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.case_id
#table employee
class Employee(models.Model):
    employee_id = models.CharField(max_length=100)
    mail = models.CharField(max_length=100)
    rights = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.employee_id
#table request  
class Request(models.Model):
    request_id = models.IntegerField()
    case_id = models.CharField()
    date_received = models.DateField()
    employee_id = models.CharField()
    status = models.CharField()

    def __str__(self):
        return self.request_id