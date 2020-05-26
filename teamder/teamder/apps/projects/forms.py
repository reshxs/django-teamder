from django import forms
from .models import Project, Technology


class ProjectForm(forms.ModelForm):
	project_name = forms.CharField(max_length=50, label='Название проекта')
	project_description = forms.TextInput()
	members_count = forms.IntegerField(label='Количество участников')

	class Meta:
		model = Project
		fields = ('project_name', 'project_description', 'members_count')
