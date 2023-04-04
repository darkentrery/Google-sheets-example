from django.urls import path

from google_sheets.supplies import views

urlpatterns = [
    path("get-supplies/", views.SuppliesView.as_view(), name='get-supplies'),
]