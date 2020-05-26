from django.http import Http404, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import UserAccount
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


def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        bio = request.POST.get('bio')

        user = User(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
        user.save()
        useraccount = user.useraccount
        useraccount.user_bio = bio
        useraccount.save()
        return redirect("/")
    else:
        form = RegistrationForm
        return render(request, 'registration/registration_form.html', {'form': form})


@login_required
def configure(request, user_id):
    # Сделать вьюшку для редактирования профиля
    return HttpResponse('Тут вы смодете редактировать ваш профиль!')
