from typing import Any

from django.db.models import Count, Max, OuterRef, Subquery
from django.db.models.functions import Coalesce, Greatest
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.views import generic

from .forms import CommentForm, MessageForm
from .models import Comment, Message, Tag, Topic

# def index(request):
#     TOPIC_LIST = (
#         Topic.objects.all()
#         .annotate(
#             latest_message_date=Max("topic_message__created_at"),
#             latest_comment_date=Max("topic_message__comment_created_at"),
#             latest_date=Greatest("latest_date", "latest_message_date"),
#             time=Coalesce("latest_date", "last_message_date", "last_comment_date"),
#         )
#         .order_by("-time")
#     )
#     context = {
#         "topics": TOPIC_LIST,
#     }
#     return render(request, "forum/index.html", context)


class IndexView(generic.ListView):
    template_name = "forum/index.html"
    model = Topic
    context_object_name = "topics"

    def get_queryset(self):
        queryset = (
            Topic.objects.all()
            .annotate(
                latest_message_date=Max("topic_message__created_at"),
                latest_comment_date=Max("topic_message__comment__created_at"),
                latest_date=Greatest("latest_comment_date", "latest_message_date"),
                time=Coalesce(
                    "latest_date", "latest_message_date", "latest_comment_date"
                ),
            )
            .order_by("-time")
        )
        return queryset


# def forum(request, topic):
#     topic = Topic.objects.get(name=topic)
#     messages = (
#         Message.objects.filter(topic=topic)
#         .annotate(
#             reply_num=Count("comment"), latest_reply_date=Max("comment__created_at")
#         )
#         .prefetch_related("tag", "comment")
#         .order_by("created_at")
#     )

#     if request.method == "POST":
#         if request.user.is_authenticated:
#             if "message" in request.POST:
#                 message_form = MessageForm(request.POST)
#                 if message_form.is_valid():
#                     message_form.instance.topic = topic
#                     message_form.instance.user = request.user
#                     message = message_form.save()
#                     for tag in message_form.cleaned_data["tag"]:
#                         message.tag.add(tag)
#             elif "comment" in request.POST:
#                 comment_form = CommentForm(request.POST)
#                 if comment_form.is_valid():
#                     message_id = request.POST["comment"]
#                     message = Message.objects.get(id=message_id)
#                     # 保存前のformが生成するインスタンスにアクセスする
#                     comment_form.instance.message = message
#                     comment_form.instance.user = request.user
#                     comment_form.save()
#             return redirect("forum:forum", topic=topic.name)
#     comment_form = CommentForm()
#     message_form = MessageForm()
#     context = {
#         "messages": messages,
#         "topic": topic,
#         "comment_form": comment_form,
#         "message_form": message_form,
#     }

#     return render(request, "forum/forum.html", context)


class ForumView(generic.ListView):
    template_name = "forum/forum.html"
    context_object_name = "messages"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        topic = Topic.objects.get(name=self.kwargs["topic"])
        context["topic"] = topic

        context["message_form"] = MessageForm()
        context["comment_form"] = CommentForm()

        return context

    def get_queryset(self):
        topic = Topic.objects.get(name=self.kwargs["topic"])
        subquery = Comment.objects.filter(message=OuterRef("id")).order_by(
            "-created_at"
        )
        queryset = (
            Message.objects.filter(topic=topic)
            .annotate(
                reply_num=Count("comment"),
                latest_reply_date=Subquery(subquery.values("created_at")[:1]),
            )
            .prefetch_related("tag", "comment")
            .order_by("created_at")
        )
        print(queryset)
        return queryset

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            topic = Topic.objects.get(name=self.kwargs["topic"])

            if "message" in request.POST:
                message_form = MessageForm(request.POST, request.FILES)

                if message_form.is_valid():
                    message_form.instance.topic = topic
                    message_form.instance.user = request.user
                    message = message_form.save()
                    for tag in message_form.cleaned_data["tag"]:
                        message.tag.add(tag)

            elif "comment" in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    message_id = request.POST["comment"]
                    message = Message.objects.get(id=message_id)

                    comment_form.instance.message = message
                    comment_form.instance.user = request.user
                    comment_form.save()

            return redirect("forum:forum", topic=topic.name)

        else:
            return redirect("forum:forum", topic=self.kwargs["topic"])
