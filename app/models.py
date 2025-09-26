from django.db import models

class Ticket(models.Model):
    subject = models.CharField(max_length=225,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    file_attachment = models.ImageField(upload_to="images/",blank=True,null=True)
    priority = models.CharField(max_length=225,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Crm(models.Model):
    name = models.CharField(max_length=225,blank=True,null=True)
    client_name = models.CharField(max_length=225,blank=True,null=True)
    project_value = models.CharField(max_length=225,blank=True,null=True)
    software = models.CharField(max_length=225,blank=True,null=True)
    status = models.CharField(max_length=225,blank=True,null=True)
    start_date_time = models.CharField(max_length=225,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class AdminPayments(models.Model):
    employee_id = models.CharField(max_length=225,blank=True,null=True)
    client_name = models.CharField(max_length=225,blank=True,null=True)
    Contact_person = models.CharField(max_length=225,blank=True,null=True)
    project_amount = models.CharField(max_length=225,blank=True,null=True)
    my_commission = models.CharField(max_length=225,blank=True,null=True)
    my_percentage = models.CharField(max_length=225,blank=True,null=True)
    total_pay = models.CharField(max_length=225,blank=True,null=True)
    withdraw_payment = models.CharField(max_length=225,blank=True,null=True)


class AdminEmployeeRegister(models.Model):
    name = models.CharField(max_length=225,blank=True,null=True)
    email = models.CharField(max_length=225,blank=True,null=True)
    role = models.CharField(max_length=225,blank=True,null=True)
    phone =models.CharField(max_length=225,blank=True,null=True)

from django.db import models
import random
import string

 


class Fieldwork(models.Model):
    field_name = models.CharField(max_length=100,blank=True,null=True)
    timestamp  = models.CharField(max_length=100,blank=True,null=True)
    location = models.CharField(max_length=100,blank=True,null=True)
    purpose = models.CharField(max_length=100,blank=True,null=True)
    upload_photos = models.ImageField(upload_to="field_work/",blank=True,null=True)
    lead_status = models.CharField(max_length=100,blank=True,null=True)
    project_value = models.CharField(max_length=100,blank=True,null=True)
    
class BillsUpload(models.Model):  
    Upload_all_bills = models.FileField(upload_to="pdfs/",blank=True,null=True)


from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# --- Custom Manager ---
class EmployeeManager(BaseUserManager):
    def create_user(self, employee_id, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Employees must have an email address")
        email = self.normalize_email(email)
        user = self.model(employee_id=employee_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(employee_id, email, password, **extra_fields)


# --- Employee Model ---
class Employee(AbstractBaseUser, PermissionsMixin):
    employee_id = models.CharField(max_length=10, unique=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = "employee_id"
    REQUIRED_FIELDS = ["email"]

    def save(self, *args, **kwargs):
        if not self.employee_id:
            last_employee = Employee.objects.order_by('id').last()
            if last_employee:
                last_id = int(last_employee.employee_id[3:])
                new_id = last_id + 1
            else:
                new_id = 1
            self.employee_id = f"TIT{new_id:04d}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} - {self.name}"





