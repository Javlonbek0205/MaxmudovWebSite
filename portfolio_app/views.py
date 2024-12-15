from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import User
from .forms import CommentForm, ContactForm
from portfolio_app.models import Portfolio, PortfolioLike, Comment, Tag, Technology, PortfolioLink, PortfolioImage
from blog_app.models import Article
from accounts.utils.email_verification import RedisDataStore
# Create your views here.
def home_view(request):
    portfolios = Portfolio.objects.all()
    contact_form = None
    articles = Article.objects.order_by('-created_at')[:3]
    user_count = User.objects.count()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your message has been sent.')
        else:
            return redirect('home')
    context = {
        'portfolios': portfolios,
        'user_count': user_count,
        'articles': articles,
        'contact_form': contact_form,
    }
    return render(request, 'index.html', context)


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
        if not request.user.is_authenticated:
            return redirect('login')

        if not request.user.is_email_verified:
            if RedisDataStore.is_expired(f'ev:{request.user.email}'):
                RedisDataStore.send_verification_code(request.user.email)
            return redirect('email_verification')

        if 'like' in request.POST:
            if user_has_liked:
                PortfolioLike.objects.filter(portfolio=portfolio, user=request.user).delete()
                messages.success(request, 'You have already liked this portfolio.')
            else:
                PortfolioLike.objects.create(portfolio=portfolio, user=request.user)
                messages.success(request, 'You have liked this portfolio.')
        elif 'comment' in request.POST and comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.portfolio = portfolio
            comment.user = request.user
            comment.save()
            messages.success(request, 'Your comment has been added.')

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
