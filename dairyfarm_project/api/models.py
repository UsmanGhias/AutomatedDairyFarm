from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _



class Farm(models.Model):
    name = models.CharField(max_length=100)
    expense_tracking = models.DecimalField(max_digits=8, decimal_places=2)
    revenue_calculation = models.DecimalField(max_digits=8, decimal_places=2)

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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(Group, related_name='custom_user_set', related_query_name='custom_user')
    user_permissions = models.ManyToManyField(
        Permission, related_name='custom_user_set', related_query_name='custom_user'
    )

    def __str__(self):
        return self.email


class Vendor(models.Model):
    managername = models.CharField(max_length=200)
    vendorname = models.CharField(max_length=200, db_index=True, unique=True)
    joiningdate = models.DateField(auto_now_add=True)
    address = models.CharField(max_length=200, db_index=True)
    vendorcontact = models.CharField(max_length=14, db_index=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.vendorname


class MilkCategory(models.Model):
    ANIMAL_CHOICES = (
        ('Cow', 'Cow'),
        ('Buffaloe', 'Buffalo'),
        ('Others', 'Others'),
    )
    animalname = models.CharField(max_length=200, choices=ANIMAL_CHOICES)
    milkprice = models.FloatField(max_length=200, db_index=True)
    related_vendor = models.ForeignKey(Vendor, related_name='milk_categories', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.animalname} - {self.milkprice} Tk."


class VendorLedger(models.Model):
    related_vendor = models.ForeignKey(Vendor, related_name='ledger_entries', on_delete=models.CASCADE, null=True)
    related_milk_category = models.ForeignKey(MilkCategory, related_name='vendor_ledger', on_delete=models.CASCADE, null=True)
    date = models.DateField()
    price = models.FloatField(default=0.0)
    quantity = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)

    class Meta:
        ordering = ('-date',)


class Profile(models.Model):
    USER_TYPE_CHOICES = (
        ('Admin', 'Admin'),
        ('Customer', 'Customer'),
        ('Manager', 'Manager'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, null=True, blank=False, choices=USER_TYPE_CHOICES)
    contact_number = models.CharField(max_length=20, null=True, unique=True)
    joining_date = models.DateField(auto_now_add=False)
    address = models.CharField(max_length=500, null=True)

    class Meta:
        ordering = ('-user_type',)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class CustomerMilkCategory(models.Model):
    ANIMAL_CHOICES = (
        ('Cow', 'Cow'),
        ('Buffaloe', 'Buffalo'),
        ('Others', 'Others'),
    )
    animalname = models.CharField(max_length=200, choices=ANIMAL_CHOICES)
    milkprice = models.FloatField(max_length=200, db_index=True)
    related_customer = models.ForeignKey(User, related_name='milk_categories', on_delete=models.CASCADE, null=True)

    def fullname(self):
        return f"{self.related_customer.first_name} {self.related_customer.last_name}"

    def __str__(self):
        return f"{self.related_customer}: ({self.animalname}, {self.milkprice}) Tk."


class CustomerLedger(models.Model):
    related_milk_category = models.ForeignKey(CustomerMilkCategory, related_name='ledger_entries', on_delete=models.CASCADE, null=True)
    related_customer = models.ForeignKey(User, related_name='ledger_entries', on_delete=models.CASCADE, null=True)
    date = models.DateField()
    price = models.FloatField(default=0.0)
    quantity = models.FloatField(default=0.0)
    total = models.FloatField(default=0.0)
