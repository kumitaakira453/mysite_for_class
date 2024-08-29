from django import forms

from .models import Comment, Message, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "content",
        ]


class MessageForm(forms.ModelForm):
    def label_form_instance(self, obj):
        return obj.name

    # modelsには定義していないものも追加可能
    tag = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Message
        fields = [
            "content",
        ]
