# nlpcalculator/urls.py
from django.urls import path
from nlpcalculator import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.HomeView.as_view()),
]