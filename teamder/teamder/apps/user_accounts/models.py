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

    @receiver(post_save, sender=get_user_model())
    def create_user_account(sender, instance, created, **kwargs):
        if created:
            UserAccount.objects.create(user=instance)

    @receiver(post_save, sender=get_user_model())
    def save_user_account(sender, instance, created, **kwargs):
        instance.useraccount.save()

    @receiver(post_save, sender=Project)
    def update_current_project(sender, instance, created, **kwargs):
        ua = instance.creator.useraccount

        if created:
            ua.user_current_project = instance
        if instance.is_done:
            ua.user_current_project = None

        ua.user_projects.add(instance)
        ua.save()

    # временно не рабочий метод =(
    @receiver(post_save, sender=Project)
    def update_members_projects(sender, instance, created, **kwargs):
        for member in instance.members.all():
            m = member.useraccount
            m.user_projects.add(instance)

            if instance.is_done:
                m.current_project = None
            else:
                m.current_project = instance

            m.save()

    def is_busy(self):
        return self.user_current_project is not None

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'
