from django.contrib import admin
from django.db import models

from .models import PayrollPeriod, PayrollItem


@admin.register(PayrollPeriod)
class PayrollPeriodAdmin(admin.ModelAdmin):

    list_display = (
        "organization",
        "name",
        "start_date",
        "end_date",
        "status",
    )

    list_filter = (
        "status",
        "organization",
    )

    search_fields = (
        "name",
        "organization__name",
    )

    date_hierarchy = "start_date"

    actions = ["calculate_selected_payroll"]

    @admin.action(description="Calculate selected payroll")
    def calculate_selected_payroll(self, request, queryset):

        for payroll_period in queryset:
            payroll_period.calculate_payroll()

        self.message_user(
            request,
            "Payroll calculated successfully."
        )


@admin.register(PayrollItem)
class PayrollItemAdmin(admin.ModelAdmin):

    list_display = (
        "employee_name",
        "employment_type",
        "days_worked",
        "basic_pay",
        "allowances",
        "deductions",
        "gross_pay",
        "net_pay",
    )

    list_filter = (
        "payroll_period",
        "employee__employment_type",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__phone",
    )

    def employee_name(self, obj):
        return f"{obj.employee.first_name} {obj.employee.last_name}"

    employee_name.short_description = "Employee"

    def employment_type(self, obj):
        return obj.employee.employment_type

    employment_type.short_description = "Type"

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context,
        )

        try:
            queryset = response.context_data["cl"].queryset

            totals = queryset.aggregate(
                total_basic=models.Sum("basic_pay"),
                total_allowances=models.Sum("allowances"),
                total_deductions=models.Sum("deductions"),
                total_gross=models.Sum("gross_pay"),
                total_net=models.Sum("net_pay"),
            )

            response.context_data["totals"] = totals

        except (AttributeError, KeyError):
            pass

        return response