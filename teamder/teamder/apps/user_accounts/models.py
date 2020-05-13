from django.db import models
from django.contrib.auth import get_user_model
from projects.models import Project


class UserAccount(models.Model):
    # Тут будет привязка аккаунта к пользователю
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=0, primary_key=True)
    # Создаем необходимые поля
    user_bio = models.TextField("Описание профиля")
    user_projects = models.ManyToManyField(Project, 'Проекты', blank=True)
    user_current_project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        verbose_name='Текущий проект',
        null=True,
        blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
