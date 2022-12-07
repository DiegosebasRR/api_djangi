from django.urls import path
from . import views
  
urlpatterns = [
    path('', views.ApiOverview, name='home'),
    path('create/', views.add_users, name='add-users'),
    path('all/', views.view_users, name='view_users'),
    path('users/<int:pk>/delete/', views.delete_users, name='delete-users'),
    path('update/<int:pk>/', views.update_users, name='update-users'),
    path('all/', views.view_users, name='view_users'),
]