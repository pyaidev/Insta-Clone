from django.contrib import admin

from apps.message.models import Chat, Participant, Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "chat", "sender", "msg", "is_read")
    list_display_links = ("id", "chat")
    search_fields = ("chat", "sender", "msg")
    date_hierarchy = "created_at"


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "chat")
    list_display_links = ("id", "user")
    search_fields = ("user", "chat")
    date_hierarchy = "created_at"


class ChatAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "created_at")
    list_display_links = ("id", "name")
    search_fields = ("name",)
    date_hierarchy = "created_at"


admin.site.register(Chat, ChatAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Message, MessageAdmin)