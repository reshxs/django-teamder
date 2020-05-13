from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return HttpResponse('user')


def detail(request, user_id):
    return render(request, 'user_accounts/detail.html')
