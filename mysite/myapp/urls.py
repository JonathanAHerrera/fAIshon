from django.urls import path
from . import views

urlpatterns = [
    path('images/', views.image_list, name='image_list'),
    path('images/<int:pk>/', views.image_detail, name='image_detail'),
    path('list-bucket-files/', views.list_bucket_files, name='list_bucket_files'),
    path('get-file/<str:filename>/', views.get_file_by_name, name='get_file_by_name'),
]
