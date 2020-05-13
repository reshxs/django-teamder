from django.shortcuts import render


def index(request):
    return render(request, 'projects/list.html')


def detail(request, project_id):
    return render(request, 'projects/detail.html')
