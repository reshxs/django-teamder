# Generated by Django 3.0.5 on 2020-05-13 10:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 13, 15, 51, 0, 731713), verbose_name='дата публикции'),
        ),
    ]