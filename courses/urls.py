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

    # Favorites functionality
    path('add_to_favorites/<str:subject>/<str:course_number>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_from_favorites/<str:subject>/<str:course_number>/', views.remove_from_favorites,
         name='remove_from_favorites'),
]