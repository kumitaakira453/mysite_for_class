from django.contrib import admin
from .models import Topic, Message

# admin.site.register(Topic)
admin.site.register(Message)


# インライン設定ができるよ
class MessageInline(admin.StackedInline):
    model = Message
    extra = 2


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
