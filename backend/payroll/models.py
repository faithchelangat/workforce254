from django.db import models

from organizations.models import Organization
from employees.models import Employee


class PayrollPeriod(models.Model):

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PROCESSING = "PROCESSING", "Processing"
        APPROVED = "APPROVED", "Approved"
        PAID = "PAID", "Paid"

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="payroll_periods",
    )

    name = models.CharField(max_length=100)

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.organization} - {self.name}"


    def calculate_payroll(self):
        from decimal import Decimal
        from employees.models import Employee

        # Delete any previous payroll calculation
        self.items.all().delete()

        # Get active employees belonging to this organization
        employees = Employee.objects.filter(
            organization=self.organization,
            is_active=True,
        )

        for employee in employees:

            days_worked = Decimal("0")
            basic_pay = Decimal("0")

            # -------------------------
            # CASUAL EMPLOYEE
            # -------------------------
            if employee.employment_type == "CASUAL":

                work_records = employee.work_records.filter(
                    work_date__gte=self.start_date,
                    work_date__lte=self.end_date,
                    status="WORKED",
                )

                for record in work_records:
                    days_worked += record.days_worked

                if employee.daily_rate:
                    basic_pay = days_worked * employee.daily_rate

            # -------------------------
            # FIXED EMPLOYEE
            # -------------------------
            elif employee.employment_type == "FIXED":

                basic_pay = employee.monthly_salary or Decimal("0")

            # -------------------------
            # PAYROLL TOTALS
            # -------------------------

            allowances = Decimal("0")
            deductions = Decimal("0")

            gross_pay = basic_pay + allowances

            net_pay = gross_pay - deductions

            PayrollItem.objects.create(
                payroll_period=self,
                employee=employee,
                days_worked=days_worked,
                basic_pay=basic_pay,
                allowances=allowances,
                deductions=deductions,
                gross_pay=gross_pay,
                net_pay=net_pay,
            )

        self.status = self.Status.PROCESSING
        self.save(update_fields=["status"])

        return self.items.all()


class PayrollItem(models.Model):

    payroll_period = models.ForeignKey(
        PayrollPeriod,
        on_delete=models.CASCADE,
        related_name="items",
    )

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="payroll_items",
    )

    days_worked = models.DecimalField(
        max_digits=8,
        decimal_places=1,
        default=0,
    )

    basic_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    allowances = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    deductions = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    gross_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    net_pay = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("payroll_period", "employee")

    def __str__(self):
        return f"{self.employee} - {self.payroll_period}"


    