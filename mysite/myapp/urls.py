from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.image_list, name='image_list'),
    path('images/<int:pk>/', views.image_detail, name='image_detail'),
]
