"""
URL configuration for shorts_project
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shorts_project.analyzer.urls')),
]
