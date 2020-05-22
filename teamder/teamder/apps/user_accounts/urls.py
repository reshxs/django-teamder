from django.urls import path

from . import views

app_name = "user_accounts"
urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:user_id>/', views.detail, name='detail'),
    path('detail/<int:user_id>/conf', views.configure, name='configure')
]
