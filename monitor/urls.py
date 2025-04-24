from django.urls import path
from . import views

urlpatterns = [
    path('cameras/', views.list_cameras),
]