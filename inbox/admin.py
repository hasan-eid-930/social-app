from django.contrib import admin
from inbox.models import Conversation, Message


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('sender', 'conversation', 'body')





admin.site.register(Conversation)
admin.site.register(Message,MessageAdmin)
