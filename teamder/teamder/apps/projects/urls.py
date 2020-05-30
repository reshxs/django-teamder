from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_new, name='add_new'),
    path('detail/<int:project_id>/', views.detail, name='detail'),
    path('detail/<int:project_id>/configure', views.configurate, name='configurate')
]
