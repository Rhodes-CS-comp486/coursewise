from django.urls import path
from . import views

urlpatterns = [
    # Home and other existing paths
    path('', views.home, name='home'),
    path('instructor_history/', views.instructor_history, name='instructor_history'),
    path('<str:subject>/<str:number>/', views.course_page, name='course_page'),
    path('historical_patterns/', views.historical_pattern_analysis, name='historical_patterns'),

    # Favorites functionality paths
    path('add_to_favorites/<str:subject>/<str:course_number>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:subject>/<str:course_number>/', views.remove_from_favorites, name='remove_from_favorites'),
]