from datetime import datetime
from django.db import models
from django.contrib.auth import get_user_model


class Technology(models.Model):
    technology_name = models.CharField("название технологии", max_length=20)

    def __str__(self):
        return self.technology_name

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'


class Project(models.Model):
    project_name = models.CharField('название проекта', max_length=100)
    project_description = models.TextField('описание проекта', blank=True)
    pub_date = models.DateTimeField('дата публикции', default=datetime.now())
    technologies = models.ManyToManyField(Technology, 'технологии', blank=True)

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Member(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, default=0, primary_key=True, unique=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member_role = models.CharField('роль участника', max_length=50)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'
