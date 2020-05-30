from django.urls import path
from . import views

app_name = "user_accounts"
urlpatterns = [
    path('', views.index, name='index'),
    path('notifications/', views.notifications, name="notifications"),
    path('register/', views.RegistrationFormView.as_view(), name='register'),
    path('configure/', views.configure, name='configure'),
    path('detail/<int:user_id>/', views.detail, name='detail'),
    path('detail/me', views.detail, name='me')
]
