from django.http import Http404, HttpResponse
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

def get_order_by(query, parameter):
    if parameter == 'pub_date':
        return query.order_by('-pub_date')
    if parameter == 'name':
        return query.order_by('project_name')
    return query


def index(request):
    tech = request.GET.get('tech')
    name = request.GET.get('name')
    name = '' if name is None else name
    status = request.GET.get('done')
    order = request.GET.get('order_by')

    projects_list = get_by_tech(tech)
    projects_list = get_by_name(projects_list, name)
    projects_list = get_by_status(projects_list, status)
    projects_list = get_order_by(projects_list, order)

    technology_list = Technology.objects.order_by('technology_name')

    context = {
        'projects_list': projects_list,
        'technology_list': technology_list,
        'selected_tech': tech,
        'selected_done': status,
        'selected_name': name,
        'selected_order': order,
    }
    
    return render(request, 'projects/list.html', context)


@login_required
def detail(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        raise Http404("Проект не найден!")

    if request.method == 'POST':
        if request.POST.get('done') == 'true':
            project.is_done = True
            project.creator.useraccount.user_current_project = None
            project.creator.useraccount.user_projects.add(project)
            project.creator.useraccount.save()

            for member in project.members.all():
                member.useraccount.user_current_project = None
                member.useraccount.user_projects.add(project)
                member.useraccount.save()

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

    context = {
        'project': project,
        'member_list': member_list,
        'technology_list': technology_list,
        'empty_places_count': project.members_count - project.members.count(),
    }

    return render(request, 'projects/detail.html', context)


@login_required
def manage_members(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except:
        return Http404()

    if request.method == 'POST':
        member_id = int(request.POST.get('member_id'))
        action = request.POST.get('action')

        if action == 'delete':
            project.members.get(id=member_id).delete()

        project.save()

    if project.creator == request.user:
        members_list = project.members.all()

        context = {
            'members': members_list,
            'project_id': project.id,
        }

        return render(request, 'projects/manage_members.html', context)

    else:
        return HttpResponse('У вас нет доступа к данному действю!')


@login_required
def add_new(request):
    if request.method == "POST":
        project_name = request.POST.get('project_name')
        project_description = request.POST.get('project_description')
        pub_date = timezone.now()
        creator = request.user
        members_count = request.POST.get('members_count')
        technologies = request.POST.getlist('technologies')
        user_account = request.user.useraccount

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

        user_account.user_projects.add(a)
        user_account.user_current_project = a

        return redirect('/projects')

    else:
        technology_list = Technology.objects.order_by('technology_name')
        form = ProjectForm

        context = {
            'technology_list': technology_list,
            'form': form,
            'title': 'Создать'
        }

        return render(request, 'projects/add_new.html', context)


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

        project.technologies.clear()
        for tech in technologies:
            technology = Technology.objects.get(id=int(tech))
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

        context = {
            'technology_list': technology_list,
            'form': form,
            'title': 'Редактировать',
            'project_tech_list': project.technologies.all()
        }

        return render(request, 'projects/add_new.html', context)
