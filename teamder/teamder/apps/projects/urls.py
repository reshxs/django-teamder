from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='_index_'),
    path('<int:project_id>/', views.detail, name='detail')
]
