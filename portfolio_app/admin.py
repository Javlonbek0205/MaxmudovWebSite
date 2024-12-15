from django.contrib import admin
from .models import Portfolio, PortfolioLink, PortfolioImage, PortfolioLike, Technology, Tag, Comment
# Register your models here.
admin.site.register(Portfolio)
admin.site.register(PortfolioLink)
admin.site.register(Comment)
admin.site.register(PortfolioImage)
admin.site.register(PortfolioLike)
admin.site.register(Technology)
admin.site.register(Tag)