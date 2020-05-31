from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        user = request.user
        current_project = user.useraccount.user_current_project
        current_project_members = current_project.members.all()
        notifications_list = user.notifications.order_by('-pub_date')[:5]
        unread_notifications = len(user.notifications.filter(is_read=True))
    else:
        current_project = None
        notifications_list = None
        current_project_members = None
        unread_notifications = 0

    return render(request, 'base.html', {
        'current_project': current_project,
        'notifications_list': notifications_list,
        'unread_notifications': unread_notifications,
        'members': current_project_members
    })
