from django.http import HttpResponse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render

from .models import UserAccount

def index(request):
	user_accounts_list = UserAccount.object.order_by()
    return render(request, 'user_accounts/list.html' {'user_accounts_list': user_accounts_list})


def detail(request, user_id):
    try:
    	a = UserAccount.object.get(id = user_id)
    except:
    	raise Http404("Пользователь не найден!")
    
    return render(request, 'user_accounts/detail.html', {'user_accounts': a})
