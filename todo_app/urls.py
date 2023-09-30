from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name = 'register'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('homepage', views.homepage, name='homepage'),
    path('create-list/', views.create_list, name='create_list'),
    path('delete_list/<int:list_id>', views.delete_list, name="delete_list"),
    path('delete_task/<int:task_id>', views.delete_task, name="delete_task")
]
