from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from .models import Project


def index(request):
    projects_list = Project.objects.order_by('-pub_date')
    return render(request, 'projects/list.html', {'projects_list': projects_list})


@login_required()
def detail(request, project_id):
    try:
        a = Project.objects.get(id=project_id)
    except:
        raise Http404("Проект не найден!")

    member_list = a.member_set.all()
    technology_list = a.technologies.all()
    return render(request, 'projects/detail.html', {
        'project': a,
        'member_list': member_list,
        'technology_list': technology_list,
    })