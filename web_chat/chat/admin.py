from django.contrib import admin
from .models import Chat, Message

@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ('id',)

    def get_members(self, obj):
        return '\n'.join([m.members for m in obj.members.all()])

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'chat', 'author', 'message', 'pub_date', 'is_readed',)
