from django.forms import ModelForm
from blog_app.models.articles import ArticleComment, Article


class ArticleCommentForm(ModelForm):
    class Meta:
        model = ArticleComment
        fields = ['comment', ]


class CreateArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'body', 'image', 'category']
