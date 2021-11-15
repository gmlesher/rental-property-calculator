"""Defines URL patterns for bot."""
from django.urls import path
from . import views

app_name = 'bot'
urlpatterns = [
    # Run bot
    path('run-bot/', views.run_bot, name='run-bot'),
    # Bot Report Page
    path('bot-report/<int:pk>/', views.bot_report, name='bot-report'),
    # Bot Reports Page
    path('bot-reports/', views.bot_reports, name='bot-reports'),
    # Edit Bot Report Page
    path('bot-edit-rental-prop-calc/<int:pk>/', views.bot_edit_rental_prop_calc, name='bot-edit-rental-prop-calc'),
    # Delete Bot Report Page
    path('bot-delete-report/<int:pk>/', views.bot_delete_report, name='bot-delete-report'),
]