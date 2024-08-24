from django.contrib import admin

from .models import Choice, Question

# admin.site.register(Question)
admin.site.register(Choice)


# インライン設定ができるよ
class ChoiseInline(admin.StackedInline):
    model = Choice
    extra = 1


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiseInline]
