"""portfolio/urls.py"""

from django.urls import path
from portfolio import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.projects, name='projects'),
    path('<slug:slug>/', views.project_detail, name='project_detail'),
]
