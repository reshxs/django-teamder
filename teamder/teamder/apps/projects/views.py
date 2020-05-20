from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project, Technology


def filter_objects(filter_parameter):
    result = Project.objects

    f = filter_parameter.split('?')
    for parameter in f:
        if parameter != '':
            parameter = parameter.split('=')
            if parameter[0] == 'name':
                for req in parameter[1].split('+'):
                    result = result.filter(project_name__icontains=req)
            if parameter[0] == 'done':
                result = result.filter(is_done=parameter[1] == 'true')

    return result.order_by('-pub_date')


def index(request, filter_request=''):
    if filter_request != '':
        projects_list = filter_objects(filter_request)
    else:
        projects_list = Project.objects.order_by('-pub_date')
    return render(request, 'projects/list.html', {'projects_list': projects_list})


@login_required
def detail(request, project_id):
    try:
        a = Project.objects.get(id=project_id)
    except:
        raise Http404("Проект не найден!")

    member_list = a.members.all()
    technology_list = a.technologies.all()
    return render(request, 'projects/detail.html', {
        'project': a,
        'member_list': member_list,
        'technology_list': technology_list,
    })


@login_required
def add_new(request):
    return HttpResponse('Тут можно будет создать объявление')
