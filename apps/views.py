from datetime import timedelta
import random
from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView, TemplateView
from redis import Redis

from apps.forms import EmailForm, RegisterModelForm, LoginForm


class SendMailFormView(FormView):
    form_class = EmailForm
    template_name = 'apps/auth/register.html'
    success_url = reverse_lazy('check_email')

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        verify_code = random.randrange(10 ** 5, 10 ** 6)
        send_mail(
            subject="Verification Code !!!",
            message=f"{verify_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )
        redis = Redis()
        try:
            redis.set(email, verify_code)
            redis.expire(email, time=timedelta(minutes=5))
        finally:
            redis.close()

        return render(self.request, 'apps/auth/check_message.html', {"email": email})

    def form_invalid(self, form):
        for error in form.errors.values():
            messages().error(self.request, error)
        return super().form_invalid(form)


class RegisterCreateView(CreateView):
    form_class = RegisterModelForm
    template_name = 'apps/auth/register.html'
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        sms_code = form.cleaned_data.get('sms')
        redis = Redis()
        try:
            redis_code = redis.get(email)
            if not redis_code:
                messages.error(self.request, "Kod muddati tugagan.")
                return redirect('check_email')

            if int(redis_code) != int(sms_code):
                messages.error(self.request, "Kod noto'g'ri !!!")
                return redirect(reverse_lazy('send_email'))

            user = form.save()

            login(self.request, user)

            return redirect(self.success_url)
        finally:
            redis.close()

class LoginFormView(FormView):
    form_class = LoginForm
    template_name = 'apps/auth/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Authenticate the user
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Email yoki parol noto‘g‘ri')
            return redirect('login1')

    def form_invalid(self, form):
        messages.error(self.request, 'Iltimos, barcha maydonlarni to‘g‘ri to‘ldiring')
        return super().form_invalid(form)

class HomeView(TemplateView):
    template_name = 'apps/web/base.html'

class TextView(TemplateView):
    template_name = 'apps/web/text.html'

class LogoutView(TemplateView):
    template_name = 'apps/auth/login.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
