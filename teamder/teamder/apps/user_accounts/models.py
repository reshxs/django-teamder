from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from projects.models import Project


class UserAccount(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=0, primary_key=True)
    user_bio = models.TextField("Описание профиля")
    user_projects = models.ManyToManyField(Project, 'Проекты', blank=True)
    user_current_project = models.ForeignKey(
        Project,
        on_delete=models.SET_NULL,
        verbose_name='Текущий проект',
        null=True,
        blank=True)

    # Автоматическое обновление модели UserAccount при создании/изменении модели user
    @receiver(post_save, sender=get_user_model())
    def create_user_account(sender, instance, created, **kwargs):
        if created:
            UserAccount.objects.create(user=instance)

    @receiver(post_save, sender=get_user_model())
    def save_user_account(sender, instance, created, **kwargs):
        instance.useraccount.save()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
