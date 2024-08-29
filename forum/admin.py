from django.contrib import admin

from .models import Comment, Message, Tag, Topic

admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Comment)
admin.site.register(Tag)
