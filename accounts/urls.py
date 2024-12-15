from django.urls import path
from .views import UserCreate

urlpatterns = [
    path('signup/', UserCreate.as_view() , name='signup'),
]