from django.shortcuts import render, redirect
from .models import Notification



def ShowNotification(request):
    notifications = Notification.objects.all()
    print(notifications[0].post.post_medias.all()[0].file.url)


    context = {
        'notifications': notifications,

    }
    print(context)
    return render(request, 'notification/notification.html', context)


def DeleteNotification(request, noti_id):
    user = request.user
    Notification.objects.filter(id=noti_id, user=user).delete()
    return redirect('show-notification')
