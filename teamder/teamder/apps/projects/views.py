from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import Project, Member, Technology

def index(request):
	projects_list = Project.objects.order_by('-pub_date')
    return render(request, 'projects/list.html', {'projects_list': projects_list})

def detail(request, project_id):
	try:
		a = Project.objects.get(id = project_id )
	except:
		raise Http404("Проект не найден!")

	member_list = a.member_set.order_by()
	technology_list = a.technology_set.order_by()
 	return render(request, 'projects/detail.html', {'project': a, 'technology_list': technology_list, 'member_list': member_list})
