from django import forms
from .models import Project, Technology


class ProjectForm(forms.ModelForm):
	project_name = forms.CharField(max_length=50, label='Название проекта', widget=forms.TextInput(attrs={
		"placeholder": "Название проекта",
		"class": "form-control"
	}))
	project_description = forms.CharField(max_length=500, label='Описание проекта', widget=forms.Textarea(attrs={
		"placeholder": "Описание проекта",
		"class": "form-control",
		"rows": "4"
	}))
	members_count = forms.IntegerField(label='Количество участников', widget=forms.NumberInput(attrs={
		"placeholder": "Количество участников",
		"class": "form-control"
	}))
	tech_choiсes = enumerate(Technology.objects.all())
	technologies = forms.MultipleChoiceField(label='Выберите используемые технологии', choices=tech_choiсes)

	class Meta:
		model = Project
		fields = ('project_name', 'project_description', 'members_count', 'technologies')
