from django.urls import path
from . import views

urlpatterns = [
    path('ipcameras/', views.list_cameras),
    path('ipcamera/create/', views.create_ipcamera, name='create_ipcamera'),
    path('ipcamera/<str:camera_id>/', views.get_ipcamera, name='get_ipcamera'),
    path('ipcamera/<str:camera_id>/update/', views.update_ipcamera, name='update_ipcamera'),
    path('ipcamera/<str:camera_id>/delete/', views.delete_ipcamera, name='delete_ipcamera'),
]