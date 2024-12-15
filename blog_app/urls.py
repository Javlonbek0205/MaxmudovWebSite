from django.urls import path
from .views import blog_list_view, blog_detail_view, create_article

urlpatterns = [
    path('', blog_list_view, name='blog_list'),
    path('create/', create_article, name='blog_create'),
    path('<int:pk>/', blog_detail_view, name='blog_detail'),
]