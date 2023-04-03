from django.contrib import admin

from google_sheets.supplies.models import Supply


@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = [
        "number",
        "order",
        "cost",
        "date",
        "cost_rub",
    ]
