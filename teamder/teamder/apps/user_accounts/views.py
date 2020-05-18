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
        user_account = user.useraccount
    except:
        raise Http404("Пользователь не найден!")

    user_projects = user_account.user_projects.all()
    user_current_project = user_account.user_current_project

    return render(request, 'user_accounts/detail.html', {
        'user_account': user_account,
        'user_projects': user_projects,
        'user_current_project': user_current_project,
    })
