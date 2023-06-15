
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('dairyapp.urls')),  # Use 'api/' as a prefix for your API endpoints
]
