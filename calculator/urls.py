"""Defines URL patterns for calculator."""
from django.urls import path
from . import views

app_name = 'calculator'
urlpatterns = [
    # Home Page
    path('', views.index, name='index'),
<<<<<<< Updated upstream
=======
    # Dashboard Page
    path('dashboard/', views.dashboard, name='dashboard'),
    # Reports Page
    path('reports/', views.reports, name='reports'),
>>>>>>> Stashed changes
    # Calculator Page
    path('rental-prop-calculator/', views.rental_prop_calculator, name='rental-prop-calculator'),
    # Report Page
    path('report/<int:pk>/', views.report, name='report'),
    # Edit Report Page
    path('edit-rental-prop-calc/<int:pk>/', views.edit_rental_prop_calc, name='edit-rental-prop-calc'),
    # Delete Report Page
    path('delete-report/<int:pk>/', views.delete_report, name='delete-report'),
]