from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project, Technology


def parse_request(request, parameter):
    result = request.GET.get(parameter)
    return result if result is not None else ''


def index(request):
    tech = parse_request(request, 'tech')
    name = parse_request(request, 'name')
    projects_list = Project.objects.filter(project_name__icontains=name).order_by('-pub_date')
    technology_list = Technology.objects.all()
    return render(request, 'projects/list.html', {
        'projects_list': projects_list,
        'technology_list': technology_list
    })


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
