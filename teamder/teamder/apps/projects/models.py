import datetime
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class Ad(models.Model):
    ad_pub_date = models.DateTimeField('дата публикации')

    # РАЗОБАРТЬСЯ ПОЧЕМУ НЕ РАБОТАИИИТ:
    # def was_published_recently(self):
    #  return self.ad_pub_date >= (timezone.now() - datetime.timedelta(days=14))

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


#class Member(models.Model):
#    member_name = models.CharField('имя участника', max_length=50)
#    member_role = models.CharField('роль участника', max_length=50)
#
#    def __str__(self):
#        return self.member_name
#
#    class Meta:
#        verbose_name = 'Участник'
#        verbose_name_plural = 'Участники'


class Technology(models.Model):
    technology_name = models.CharField("название технологии", max_length=20)

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'


class Project(models.Model):
    project_name = models.CharField('название проекта', max_length=100)
    project_description = models.TextField('описание проекта')
    project_members = models.ManyToManyField(get_user_model())
    project_technologies = models.ManyToManyField(Technology)
    default_Ad = Ad
    default_Ad.ad_pub_date = datetime.datetime.now()
    project_Ad = models.OneToOneField(Ad, on_delete=models.CASCADE, default=default_Ad)


    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
