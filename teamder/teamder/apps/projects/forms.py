from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project
		fields = ('project_name', 'project_description', 'pub_date', 'creator', 'members_count', 'technologies')