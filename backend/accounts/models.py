from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Admin"
        COMPANY_ADMIN = "COMPANY_ADMIN", "Company Admin"
        HR = "HR", "HR"
        PAYROLL = "PAYROLL", "Payroll"
        SUPERVISOR = "SUPERVISOR", "Supervisor"
        EMPLOYEE = "EMPLOYEE", "Employee"

    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=30, blank=True, null=True)

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="users",
        null=True,
        blank=True,
    )

    role = models.CharField(
        max_length=30,
        choices=Role.choices,
        default=Role.EMPLOYEE,
    )

    def __str__(self):
        return self.username