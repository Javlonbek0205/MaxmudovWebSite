from django.conf import settings
from django.http import JsonResponse

from accounts.models import User
from django.core.validators import FileExtensionValidator
from django.db import models

from portfolio_app.services import send_email


class Technology(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Portfolio(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    packages = models.TextField()
    image = models.ImageField(upload_to='portfolio/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'webp'])])
    technologies = models.ManyToManyField(Technology, related_name='portfolios', blank=True)
    tags = models.ManyToManyField(Tag, related_name='portfolios', blank=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def total_comments(self):
        return self.comment_set.count()

    @property
    def total_likes(self):
        return self.portfoliolike_set.count()

class PortfolioImage(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio/gallery/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg', 'webp'])])
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.portfolio.title} - Image"

class PortfolioLink(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='links')
    url = models.URLField()
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.name or 'Link'} - {self.portfolio.title}"

class Comment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.portfolio}"

class PortfolioLike(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'portfolio'], name='unique_user_portfolio_like')
        ]
    def __str__(self):
        return f"{self.user} - {self.portfolio}"

class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    class Meta:
        get_latest_by = 'pk'
    def __str__(self):
        return self.name

    def send_mail(self):
        subject = f'New Message from {self.email}'
        email = "javlonbekmaxmudov8384@gmail.com"

        context = {
            'latest_user': self.name,
            'message': self.message
        }
        if not subject:
            return JsonResponse({'status': False, 'error': 'Subject cannot be empty'}, status=400)
        elif not email:
            return JsonResponse({'status': False, 'error': 'Email cannot be empty'}, status=400)

        send_email('send_email.html', subject, email, context)
        return JsonResponse({'status': True, 'message': 'Email sent successfully'}, status=200)
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or self._state.db == 'default':
            self.send_mail()
