from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Project, Technology

from .forms import ProjectForm
from django.views import View
from django.utils import timezone

class ProjectForm(View):
    def post(self, request):
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        pub_date = datetime.now()
        creator = request.user
        members_count = request.POST.get('members_count')
        technologies = request.POST.get('technologies')
        a = Project(project_name = project_name, 
            project_description = project_description, 
            pub_date = pub_date,
            creator = creator,
            members_count = members_count,
            technologies = technologies)
        a.save()
        return render(request,'/', {})
        
def get_by_tech(parameter):
    return Technology.objects.get(technology_name=parameter).project_set.all() \
        if parameter != "" and parameter is not None else Project.objects.all()


def get_by_name(query, parameter):
    return query.filter(project_name__icontains=parameter) if parameter is not None else query


def get_by_status(query, parameter):
    if parameter == 'true':
        return query.filter(is_done=True)
    elif parameter == 'false':
        return query.filter(is_done=False)
    else:
        return query


def index(request):
    # Собираем данные из request
    tech = request.GET.get('tech')
    name = request.GET.get('name')
    status = request.GET.get('done')

    # Фильтруем список
    projects_list = get_by_tech(tech)
    projects_list = get_by_name(projects_list, name)
    projects_list = get_by_status(projects_list, status)
    projects_list = projects_list.order_by('-pub_date')

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
    technology_list = Technology.objects.all()
    return render(request, 'projects/add_new.html', {'technology_list': technology_list})
