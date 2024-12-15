from accounts.models import CustomUser
from django.core.validators import FileExtensionValidator
from django.db import models

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
    views = models.PositiveIntegerField(default=0, editable=False)

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
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.portfolio}"

class PortfolioLike(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    liked_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'portfolio'], name='unique_user_portfolio_like')
        ]
    def __str__(self):
        return f"{self.user} - {self.portfolio}"
