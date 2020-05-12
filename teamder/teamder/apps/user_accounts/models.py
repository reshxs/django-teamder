from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserAccount(models.Model):
    # Тут будет привязка аккаунта к пользователю
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=0, primary_key=True)
    # Создаем необходимые поля
    user_description = models.TextField("Описание профиля")

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Skill(models.Model):
    # Привяжем скиллы к пользователю
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)

    # название скила
    skill_name = models.CharField("Навык", max_length=20)
