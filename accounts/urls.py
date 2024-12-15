from django.urls import path

from accounts.views import AuthFormView, RegisterFormView, VerifyEmailFormView, ResendVerificationCodeView

urlpatterns = [
    path('login/', AuthFormView.as_view(), name='login'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('verification/', VerifyEmailFormView.as_view(), name='email_verification'),
    path('verify/resend/', ResendVerificationCodeView.as_view(), name='resend_verification_code'),  # ALohida View
]