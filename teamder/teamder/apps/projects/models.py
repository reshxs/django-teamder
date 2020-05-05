import datetime
from django.db import models

from django.utils import timezone


class Project(models.Model):
    project_name = models.CharField('название проекта', max_length=100)
    project_description = models.TextField('описание проекта')

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Ad(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    ad_pub_date = models.DateTimeField('дата публикации')

    #РАЗОБАРТЬСЯ ПОЧЕМУ НЕ РАБОТАИИИТ:
    #def was_published_recently(self):
    #  return self.ad_pub_date >= (timezone.now() - datetime.timedelta(days=14))

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Member(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member_name = models.CharField('имя участника', max_length=50)
    member_role = models.CharField('роль участника', max_length=50)

    def __str__(self):
        return self.member_name

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
