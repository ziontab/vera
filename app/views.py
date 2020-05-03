from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView as ContribLoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from app import models


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = models.Article.objects.all()
        return context


class WardAddView(LoginRequiredMixin, TemplateView):
    template_name = "ward_add.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diseases'] = models.Disease.objects.all()
        return context


class LoginView(ContribLoginView):
    template_name = "login.html"


class SignupView(TemplateView):
    template_name = "signup.html"
