# Generated by Django 3.0.5 on 2020-05-13 11:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20200513_1629'),
        ('user_accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='useraccount',
            name='user_current_project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='projects.Project', verbose_name='Текущий проект'),
        ),
        migrations.AlterField(
            model_name='useraccount',
            name='user_projects',
            field=models.ManyToManyField(blank=True, related_name='Проекты', to='projects.Project'),
        ),
    ]