from django.db import models


class UserAccount(models.Model):
    user_first_name = models.CharField("Имя пользователя", max_legth=25)
    user_last_name = models.CharField("Фамилия пользователя", max_length=25)
    user_description = models.TextField("Описание профиля")

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
