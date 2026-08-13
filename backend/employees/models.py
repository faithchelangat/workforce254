from django.db import models
from organizations.models import Organization

# Create your models here.
class Employee(models.Model):
    class EmploymentType(models.TextChoices):
        FIXED = 'FIXED', 'Fixed Employee'
        CASUAL = 'CASUAL', 'Casual Employee'

    class PaymentMethod(models.TextChoices):
        MPESA = 'MPESA', 'M-pesa',
        CASH = 'CASH', 'Cash',
        BANK = 'BANK', 'Bank'


    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="employees",

    )

    employee_number = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=30)
    national_id = models.CharField(
        max_length=30,
        null=True,
        blank=True
    )

    employment_type = models.CharField(
        max_length=30,
        choices=EmploymentType.choices,

    )

    job_title = models.CharField(max_length=150, blank=True)

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
    )
    daily_rate = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    null=True,
    blank=True,
)
    
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices,
        default=PaymentMethod.MPESA,
    )

    payment_account = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class WorkRecord(models.Model):

    class AttendanceStatus(models.TextChoices):
        WORKED = "WORKED", "Worked"
        ABSENT = "ABSENT", "Absent"
        OFF = "OFF", "Off Day"
        LEAVE = "LEAVE", "Leave"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="work_records",
    )

    work_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=AttendanceStatus.choices,
        default=AttendanceStatus.WORKED,
    )

    days_worked = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=1,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique_together = ("employee", "work_date")
        ordering = ["-work_date"]

    @property
    def amount(self):
        if self.status != self.AttendanceStatus.WORKED:
            return 0

        if self.employee.daily_rate is None:
            return 0

        return self.days_worked * self.employee.daily_rate
    def __str__(self):
        return f"{self.employee} - {self.work_date}"