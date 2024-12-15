from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CustomUser
from .forms import CommentForm
from portfolio_app.models import Portfolio, PortfolioLike, Comment, Tag, Technology, PortfolioLink, PortfolioImage
from blog_app.models import Article

# Create your views here.
def home_view(request):
    portfolios = Portfolio.objects.all()
    articles = Article.objects.order_by('-created_at')[:3]
    user_count = CustomUser.objects.count()
    context = {
        'portfolios': portfolios,
        'user_count': user_count,
        'articles': articles,
    }
    return render(request, 'home.html', context)


def detail_portfolio_view(request, pk):
    #for_portfolio
    portfolio = get_object_or_404(Portfolio, pk=pk)

    #for_comment
    comment_form = CommentForm(request.POST or None)

    #for_likes
    portfolio_likes = PortfolioLike.objects.filter(portfolio=portfolio).count()

    #has_liked
    if request.user.is_authenticated:
        user_has_liked = PortfolioLike.objects.filter(portfolio=portfolio, user=request.user).exists()
    else:
        user_has_liked = False

    if request.method == 'POST':
        if 'like' in request.POST and request.user.is_authenticated:
            if user_has_liked:
                PortfolioLike.objects.filter(portfolio=portfolio, user=request.user).delete()
                messages.success(request, 'You have already liked this portfolio.')
            else:
                PortfolioLike.objects.create(portfolio=portfolio, user=request.user)
                messages.success(request, 'You have liked this portfolio.')
        elif 'comment' in request.POST and comment_form.is_valid() and request.user.is_authenticated:
            comment = comment_form.save(commit=False)
            comment.portfolio = portfolio
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')
        else:
            return redirect('login')
        return redirect('details_portfolio', pk=pk)

    comments = Comment.objects.filter(portfolio=portfolio).order_by('-created_at')
    portfolio_links = PortfolioLink.objects.filter(portfolio=portfolio)
    portfolio_images = PortfolioImage.objects.filter(portfolio=portfolio)
    context = {
        'portfolio': portfolio,
        'comments': comments,
        'user_has_liked': user_has_liked,
        'comment_form': comment_form,
        'portfolio_likes': portfolio_likes,
        'portfolio_links': portfolio_links,
        'portfolio_images': portfolio_images,
    }
    return render(request, 'portfolio_detail.html', context)
