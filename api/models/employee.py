from django.contrib.auth.models import User
from django.db import models

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points = models.IntegerField()

    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = "Employees"
        db_table = "employees"
    
    def __str__(self):
        return self.user.username