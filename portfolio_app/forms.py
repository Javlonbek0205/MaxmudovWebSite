from django import forms
from .models import Comment, PortfolioLike

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]