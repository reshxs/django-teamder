from django.http import HttpResponse


def index(request):
    return HttpResponse('user')

def detail(request, user_id):
	return render(request, 'user_accounts/detail.html')
