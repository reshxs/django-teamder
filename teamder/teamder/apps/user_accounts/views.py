from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import FormView
from django.urls import reverse

from .models import Notification
from .forms import RegistrationForm, ConfigurationForm


def index(request):
    name = request.GET.get('name')
    name = name if name is not None else ''
    user_list = User.objects.filter(username__icontains=name)
    return render(request, 'user_accounts/list.html', {'user_list': user_list, 'sorted_name': name})


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
    success_url = "/"
    template_name = 'registration/registration_form.html'

    def form_valid(self, form):
        form.save()
        return super(RegistrationFormView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegistrationFormView, self).form_invalid(form)


def configure_user_param(user, param, value):
    if value is not None:
        if param == 'username':
            user.username = value
        if param == 'first_name':
            user.first_name = value
        if param == 'last_name':
            user.last_name = value
        if param == 'email':
            user.email = value
        if param == 'bio':
            user.useraccount.user_bio = value
            user.useraccount.save()

        user.save()


@login_required
def configure(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        bio = request.POST.get('bio')

        user = request.user

        configure_user_param(user, 'username', username)
        configure_user_param(user, 'first_name', first_name)
        configure_user_param(user, 'last_name', last_name)
        configure_user_param(user, 'email', email)
        configure_user_param(user, 'bio', bio)
        user.save()
        return redirect(reverse('user_accounts:detail', args=[user.id]))

    else:
        data = {
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
            'bio': request.user.useraccount.user_bio,
        }
        form = ConfigurationForm(data)
        return render(request, 'user_accounts/configurate.html', {'form': form})


@login_required
def notifications(request):
    if request.method == 'POST':
        notification_id = request.POST.get('notification_id')
        notification = Notification.objects.get(id=int(notification_id))
        project = notification.project

        project.members.add(notification.sender)
        user_account = notification.sender.useraccount
        user_account.user_current_project = project
        user_account.user_projects.add(project)
        user_account.save()
        project.save()
        notification.delete()

    notifications_list = request.user.notifications.all()
    return render(request, 'user_accounts/notifications.html', {'notifications_list': notifications_list})
