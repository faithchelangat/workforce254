from django.contrib import admin

from .models import Employee, WorkRecord


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):

    list_display = (
        "first_name",
        "last_name",
        "employment_type",
        "phone",
        "job_title",
        "organization",
        "is_active",
    )

    list_filter = (
        "employment_type",
        "organization",
        "is_active",
    )

    search_fields = (
        "first_name",
        "last_name",
        "phone",
        "employee_number",
    )


@admin.register(WorkRecord)
class WorkRecordAdmin(admin.ModelAdmin):

    list_display = (
    "employee",
    "work_date",
    "status",
    "days_worked",
    "amount",
)

    list_filter = (
        "status",
        "work_date",
    )

    search_fields = (
        "employee__first_name",
        "employee__last_name",
        "employee__phone",
    )

    date_hierarchy = "work_date"