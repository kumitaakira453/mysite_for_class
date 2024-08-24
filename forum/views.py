from django.shortcuts import render
from .models import Topic, Message


def index(request):
    TOPIC_LIST = Topic.objects.all()
    context = {
        "topics": TOPIC_LIST,
    }
    return render(request, "forum/index.html", context)


def forum(request, topic):
    topic = Topic.objects.get(name=topic)
    messages = Message.objects.filter(topic=topic).order_by("created_at")

    try:
        message = request.POST["message"]
        Message.objects.create(
            topic=topic,
            content=message,
        )
        # メッセージをデータベースに保存する処理
    except:
        pass

    return render(request, "forum/forum.html", {"messages": messages, "topic": topic})
