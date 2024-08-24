from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import Question, Choice


def index(request):
    # 新しいものから 5 個
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {
        "latest_question_list": latest_question_list,
    }
    return render(request, "polls/index.html", context)


# def result(request):
#     question_dict = {
#         "プログラミングは好きですか？": True,
#         "数学は好きですか？": True,
#         "国語は好きですか？": True,
#     }
#     context = {
#         "question_dict": question_dict,  # dict 型を渡す
#     }
#     return render(request, "polls/result.html", context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question,
    }
    return render(request, "polls/detail.html", context)


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    context = {
        "question": question,
    }
    return render(request, "polls/results.html", context)


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(
            pk=request.POST["choice"]
        )  # pk が POST の choice の値と等しいものがあれば、データベースから取得する
    except (KeyError, Choice.DoesNotExist):  # 例外処理
        # フォームを再度表示する
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # POST データを正常に処理した後は、redirect() を返します。これにより、ユーザーが「戻る」ボタンを押した場合にデータが 2 回投稿されるのを防ぎます。

        return redirect("polls:results", question.id)
