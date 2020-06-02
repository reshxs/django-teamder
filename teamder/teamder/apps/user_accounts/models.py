from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from projects.models import Project


class UserAccount(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=0, primary_key=True)
    user_bio = models.TextField("Описание профиля")
    user_projects = models.ManyToManyField(Project, 'Проекты', blank=True)
    user_friends = models.ManyToManyField(get_user_model(), related_name="friends", blank=True)
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
        try:
            instance.useraccount.user_current_project = instance.useraccount.user_projects.filter(is_done=False).latest('pub_date')
        except:
            instance.useraccount.user_current_project = None
        instance.useraccount.save()

    @property
    def is_busy(self):
        return self.user_current_project is not None

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'


class Notification(models.Model):
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='sent_notifications')
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='notifications')
    pub_date = models.DateTimeField('Время отправки')
    is_read = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return f'Пользователь {self.sender.first_name} {self.sender.last_name} ' \
               f'хочет присоедениться к вашему проекту {self.project.project_name} '

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
