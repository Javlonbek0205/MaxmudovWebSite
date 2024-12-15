from django.core.validators import FileExtensionValidator
from django.db import models
from accounts.models import User
from blog_app.models.categories import Category

class Article(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to="blog/", validators=[FileExtensionValidator(['jpg', 'png', 'jpeg', 'webp'])], blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def total_comments(self):
        return self.articlecomment_set.count()

class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.article}-{self.user}'

