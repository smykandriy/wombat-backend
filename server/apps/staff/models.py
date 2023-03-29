from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=30, unique=True)


class EmployeeRole(models.Model):
    name = models.CharField(max_length=20, primary_key=True)
    is_staff = models.BooleanField()


class EmployeeManager(BaseUserManager):
    def create_user(
            self,
            phone_number: str,
            password: str,
            role_name: str,
            first_name: str,
            last_name: str,
            email: str = None
    ):
        role = EmployeeRole.objects.get(role_name=role_name)
        employee = self.model(
            phone_number=phone_number,
            role=role,
            first_name=first_name,
            last_name=last_name,
            email=email,
            is_staff=False,
            is_superuser=False
        )
        employee.set_password(password)
        employee.save()
        return employee

    def create_superuser(self, phone_number: str, password: str, **kwargs):
        admin = self.model(phone_number=phone_number, is_staff=True, is_superuser=True, **kwargs)
        admin.set_password(password)
        admin.save()
        return admin


class Employee(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True)
    role = models.ForeignKey(EmployeeRole, on_delete=models.SET_NULL, null=True)
    USERNAME_FIELD = 'phone_number'
    objects = EmployeeManager()

    def __str__(self):
        return self.get_full_name() if not self.is_superuser else f'Admin {self.phone_number}'
