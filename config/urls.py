from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from google_sheets.supplies import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('api/supplies/', include('google_sheets.supplies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
