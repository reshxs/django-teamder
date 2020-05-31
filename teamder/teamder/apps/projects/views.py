from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from .models import Project, Technology
from .forms import ProjectForm
from user_accounts.models import Notification


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
    tech = request.GET.get('tech')
    name = request.GET.get('name')
    status = request.GET.get('done')

    projects_list = get_by_tech(tech)
    projects_list = get_by_name(projects_list, name)
    projects_list = get_by_status(projects_list, status)
    projects_list = projects_list.order_by('-pub_date')

    technology_list = Technology.objects.order_by('technology_name')
    return render(request, 'projects/list.html', {
        'projects_list': projects_list,
        'technology_list': technology_list,
    })


@login_required
def detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        raise Http404("Проект не найден!")

    if request.method == 'POST':
        if request.POST.get('done') == 'true':
            project.is_done = True
            project.save()
        else:
            notification = Notification()
            notification.project = project
            notification.sender = request.user
            notification.recipient = project.creator
            notification.pub_date = timezone.now()
            notification.save()

    member_list = project.members.all()
    technology_list = project.technologies.all()
    return render(request, 'projects/detail.html', {
        'project': project,
        'member_list': member_list,
        'technology_list': technology_list,
    })


@login_required
def add_new(request):
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        pub_date = timezone.now()
        creator = request.user
        members_count = request.POST.get('members_count')
        technologies = request.POST.getlist('technologies')

        a = Project(project_name=project_name,
                    project_description=project_description,
                    pub_date=pub_date,
                    creator=creator,
                    members_count=members_count)
        a.save()

        for tech in technologies:
            technology = Technology.objects.get(id=int(tech) + 1)
            if technology is not None:
                a.technologies.add(technology)
        a.save()

        return redirect('/projects')
    else:
        technology_list = Technology.objects.order_by('technology_name')
        form = ProjectForm
        return render(request, 'projects/add_new.html', {
            'technology_list': technology_list,
            'form': form,
            'title': 'Создать',
        })


@login_required
def configurate(request, project_id):
    project = Project.objects.get(id=project_id)
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        members_count = request.POST.get('members_count')
        technologies = request.POST.getlist('technologies')

        project.project_name = project_name
        project.project_description = project_description
        project.members_count = members_count

        for tech in technologies:
            technology = Technology.objects.get(id=int(tech) + 1)
            if technology is not None:
                project.technologies.add(technology)
        project.save()

        return redirect(reverse('projects:detail', args=[project.id]))
    else:
        technology_list = Technology.objects.order_by('technology_name')
        data = {
            'project_name': project.project_name,
            'project_description': project.project_description,
            'members_count': project.members_count
        }
        form = ProjectForm(data)
        return render(request, 'projects/add_new.html', {
            'technology_list': technology_list,
            'form': form,
            'title': 'Редактировать'
        })
