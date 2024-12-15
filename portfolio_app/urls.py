from django.urls import path
from .views import home_view, detail_portfolio_view

urlpatterns = [
    path('', home_view, name='home'),
    path('<int:pk>/', detail_portfolio_view, name='details_portfolio'),
]