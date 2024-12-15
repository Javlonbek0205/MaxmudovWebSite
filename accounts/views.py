from django.urls import reverse_lazy

from .forms import UserRegistrationForm
from .models import CustomUser
from django.views.generic import CreateView

class UserCreate(CreateView):
    model = CustomUser
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'
