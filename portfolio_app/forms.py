from django import forms
from .models import Comment, PortfolioLike, Contact


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text',]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'message']