from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class Farm(models.Model):
    name = models.CharField(max_length=100)
    expense_tracking = models.DecimalField(max_digits=8, decimal_places=2)
    revenue_calculation = models.DecimalField(max_digits=8, decimal_places=2)
    # Add more fields as per your requirements

    def __str__(self):
        return self.name

class Cow(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    health_data = models.TextField("Health Data")
    vaccination_record = models.TextField("Vaccination Record")
    milk_production = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    # password field is inherited from AbstractUser, so no need to redefine it
    # username field is removed since email is used as the username
    # related_name and related_query_name are not applicable here, they are used for related fields
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name='custom_user_set', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_set', related_query_name='custom_user')

    def __str__(self):
        return self.email
