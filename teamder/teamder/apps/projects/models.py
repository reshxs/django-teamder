from django.db import models
from django.contrib.auth import get_user_model


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

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'


class Member(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, default=0, primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member_name = models.CharField('имя участника', max_length=50)
    member_role = models.CharField('роль участника', max_length=50)

    def __str__(self):
        return self.member_name

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class Technology(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    technology_name = models.CharField("название технологии", max_length=20)

    class Meta:
        verbose_name = 'Технология'
        verbose_name_plural = 'Технологии'
