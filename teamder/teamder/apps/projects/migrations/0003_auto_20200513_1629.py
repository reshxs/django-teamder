# Generated by Django 3.0.5 on 2020-05-13 11:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20200513_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='project_description',
            field=models.TextField(blank=True, verbose_name='описание проекта'),
        ),
        migrations.AlterField(
            model_name='project',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 13, 16, 29, 20, 833424), verbose_name='дата публикции'),
        ),
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(blank=True, related_name='технологии', to='projects.Technology'),
        ),
    ]
