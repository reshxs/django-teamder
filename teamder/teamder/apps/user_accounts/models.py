from django.db import models


class UserAccount(models.Model):
    # Тут будет привязка аккаунта к пользователю

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
