"""
URL configuration for base project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
"""""
from django.urls import path
from . import views

urlpatterns = [
    #   path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('<str:subject>/<str:number>/', views.course_page, name='course_page'),
    path('instructor-history/', views.instructor_history, name='instructor_history'),

    path('hist_pattern/', views.hist_pattern, name='hist_pattern'),
]

"""

from django.urls import path
from . import views

urlpatterns = [
    #   path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('<str:subject>/<str:number>/', views.course_page, name='course_page'),
    path('instructor-history/', views.instructor_history, name='instructor_history'),
    path('historical-patterns/', views.historical_pattern_analysis, name='historical_patterns'),
    path('degree_requirements/', views.degree_requirements, name='degree_requirements'),
    path('update_progress/', views.update_progress, name='update_progress'),
    path('add_to_favorites/<str:subject>/<str:course_number>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:subject>/<str:course_number>/', views.remove_from_favorites, name='remove_from_favorites'),
# Make sure these paths are in your courses/urls.py file
    path('add_to_favorites/<str:subject>/<str:course_number>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:subject>/<str:course_number>/', views.remove_from_favorites, name='remove_from_favorites'),
]