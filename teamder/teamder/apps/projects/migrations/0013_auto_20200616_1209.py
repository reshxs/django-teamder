# Generated by Django 3.0.7 on 2020-06-16 12:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20200613_1044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='дата публикции'),
        ),
    ]