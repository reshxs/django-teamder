from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/<str:filter_request>/', views.index, name='search'),
    path('add/', views.add_new, name='add_new'),
    path('detail/<int:project_id>/', views.detail, name='detail')
]
