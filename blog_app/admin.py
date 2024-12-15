from django.contrib import admin
from blog_app.models.categories import Category
from blog_app.models.articles import Article, ArticleComment
# Register your models here.

admin.site.register(Category)
admin.site.register(Article)
admin.site.register(ArticleComment)