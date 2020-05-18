from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.models import User

from .models import UserAccount


def index(request):
    user_accounts_list = UserAccount.objects.all( )
    return render(request, 'user_accounts/list.html', {'user_accounts_list': user_accounts_list})


def detail(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except:
        raise Http404("Пользователь не найден!")

    user_projects = user.useraccount.user_projects.all()
    user_current_project = user.useraccount.user_current_project

    return render(request, 'user_accounts/detail.html', {
        'user': user,
        'user_projects': user_projects,
        'user_projects_count': user_projects.count(),
        'user_current_project': user_current_project,
    })
