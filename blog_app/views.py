from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from blog_app.forms import ArticleCommentForm, CreateArticleForm
from blog_app.models import Category, Article, ArticleComment
# Create your views here.

@login_required
def create_article(request):
    article_form = CreateArticleForm(request.POST, request.FILES or None)
    if request.method == 'POST' and article_form.is_valid():
        article = article_form.save(commit=False)
        if request.user.is_authenticated:
            article.author = request.user
        else:
            return redirect('login')
        article.save()
        return redirect('blog_list')
    context = {'article_form': article_form}
    return render(request, 'create_article.html', context)




@login_required
def blog_list_view(request):
    articles = Article.objects.all()
    context = {'articles': articles}
    return render(request, 'blog_list.html', context)

@login_required
def blog_detail_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article_comment_form = ArticleCommentForm(request.POST or None)

    if request.method == 'POST':
        if article_comment_form.is_valid():
            comment = article_comment_form.save(commit=False)
            comment.article = article
            if request.user.is_authenticated:
                comment.user = request.user
            else:
                return redirect('login')  # Tizimga kirmagan foydalanuvchini qaytarish
            comment.save()
            return redirect('blog_detail', pk=pk)
        else:
            print(article_comment_form.errors)

    article_comments = ArticleComment.objects.filter(article=article).order_by('-created_at')
    context = {
        'article': article,
        'article_comment_form': article_comment_form,
        'article_comments': article_comments,
    }
    return render(request, 'blog_detail.html', context)
