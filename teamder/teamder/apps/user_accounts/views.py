from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView

from .models import Notification
from .forms import RegistrationForm


def index(request):
    name = request.GET.get('name')
    name = name if name is not None else ''
    user_list = User.objects.filter(username__icontains=name)
    return render(request, 'user_accounts/list.html', {'user_list': user_list})


@login_required
def detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise Http404("Пользователь не найден!")

    user_projects = user.useraccount.user_projects.all()
    user_current_project = user.useraccount.user_current_project

    return render(request, 'user_accounts/detail.html', {
        'current_user': user,
        'user_projects': user_projects,
        'user_projects_count': user_projects.count(),
        'user_current_project': user_current_project,
    })


class RegistrationFormView(FormView):
    form_class = RegistrationForm
    success_url = 'configure/'
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationFormView, self).form_invalid(form)


@login_required
def notifications(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=int(notification_id))
        project = notification.project

        if len(project.members.all()) < project.members_count:
            project.members.add(notification.sender)
            user_account = notification.user.useracount
            user_account.current_project = project
            user_account.projects.add(project)
            user_account.save()
            project.save()
            notification.delete()
        else:
            HttpResponse("Лимит участников превышен!")

    notifications_list = request.user.notifications.all()
    return render(request, 'user_accounts/notifications.html', {'notifications_list': notifications_list})


@login_required
def configure(request):
    user = request.user
    user_account = user.useraccount

    if request.method == 'POST':
        username = request.POST.get('username')
        if username is not None:
            user.username = username

        first_name = request.POST.get('first_name')
        if first_name is not None:
            user.first_name = first_name

        last_name = request.POST.get('last_name')
        if last_name is not None:
            user.last_name = last_name

        email = request.POST.get('email')
        if email is not None:
            user.email = email

        user_account.bio = request.POST.get('bio')
        user.save()
        return redirect("/")

    else:
        return render(request, 'user_accounts/configurate.html', {'user_account': user_account})


def reg_configure(request):
    return HttpResponse('Создание аккаунта')
