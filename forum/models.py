from django.db import models


class Topic(models.Model):
    name = models.CharField("トピック名", max_length=20)

    def __str__(self):
        return self.name


class Message(models.Model):
    created_at = models.DateTimeField("投稿日時", auto_now_add=True)
    content = models.CharField("内容", max_length=200)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
