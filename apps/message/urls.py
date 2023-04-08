from django.urls import path


from .views import  MessageView, create_chat

app_name = 'message'

urlpatterns = [
    path("message.css/", MessageView.as_view(), name='message'),
    path("message.css/<str:name>/", MessageView.as_view(), name='message'),
    path("create_chat/<int:user_id>/", create_chat, name='create-chat'),
]