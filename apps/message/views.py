from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from apps.users.models import User
from .models import Chat, Participant


class MessageView(TemplateView):
    template_name = "accounts/chat.html"

    def get(self, request, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context['participants'] = Participant.objects.filter(~Q(user=self.request.user),
                                                             chat__participant__user=self.request.user)
        context['all_users'] = User.objects.all().exclude(id=self.request.user.id)
        try:
            name = kwargs.get('name')
            chat = get_object_or_404(Chat, name=name)
            context['chat'] = chat
            context['partner'] = Participant.objects.filter(chat=chat).exclude(user=self.request.user).first()
            messages = chat.messages.all().filter(~Q(sender=self.request.user), is_read=False)
            for message in messages:
                message.is_read = True
                message.save()
        except Exception as e:
            context['chat'] = Chat.objects.first()
        return self.render_to_response(context)


def create_chat(request, user_id):
    chat = Chat.objects.filter(participant__user=request.user).filter(participant__user__id=user_id).distinct()
    if chat.exists():
        return redirect(f'/messages/message.css/{chat.first().name}/')
    else:
        chat = Chat.objects.create()
        Participant.objects.create(user_id=user_id, chat=chat)
        Participant.objects.create(user=request.user, chat=chat)

        return redirect(f'/messages/message.css/{chat.name}/')
