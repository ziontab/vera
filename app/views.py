from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as ContribLoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from app import models, forms


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['articles'] = models.Article.objects.all()
        return context


class WardView(LoginRequiredMixin, UpdateView):
    template_name = "ward.html"
    model = models.Ward
    fields = [
        'first_name', 'middle_name', 'last_name', 'birthday', 'sex', 'address', 'phone', 'status', 'disease',
        'doctor_description', 'complaints', 'recommendations', 'description'
    ]


class WardAddView(LoginRequiredMixin, CreateView):
    template_name = "ward_add.html"

    model = models.Ward
    fields = ['first_name', 'middle_name', 'last_name', 'birthday', 'sex', 'address', 'phone', 'status', 'disease']
    success_url = '/events/'

    def form_valid(self, form):
        form.instance.nurse = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diseases'] = models.Disease.objects.all()
        return context


class EventsView(LoginRequiredMixin, TemplateView):
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = models.Event.objects.filter(nurse=self.request.user).order_by('date_planned')
        return context


class ArticleView(LoginRequiredMixin, DetailView):
    template_name = "article.html"
    model = models.Article

    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        object.add_read(self.request.user)
        return object


class ArticlesView(LoginRequiredMixin, ListView):
    template_name = "articles.html"
    model = models.Article
    paginate_by = 100

    def get_queryset(self):
        return models.Article.objects.recommend(nurse=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'recommend'
        return context


class ArticlesLikedView(ArticlesView):
    def get_queryset(self):
        return models.Article.objects.liked(nurse=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'liked'
        return context


class ArticlesReadView(ArticlesView):
    def get_queryset(self):
        return models.Article.objects.read(nurse=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'read'
        return context


class ArticlesByTagView(ArticlesView):
    def get_queryset(self):
        return models.Article.objects.by_tag(self.kwargs.get('slug'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['section'] = 'by_tag'
        return context


class LoginView(ContribLoginView):
    template_name = "login.html"


class SignupView(FormView):
    template_name = "signup.html"
    form_class = forms.SignupForm
    success_url = '/role/'

    def form_valid(self, form):
        nurse = form.save()
        login(self.request, nurse)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class RoleView(LoginRequiredMixin, UpdateView):
    template_name = "role.html"

    model = models.Nurse
    fields = ['role']
    success_url = '/ward/add/'

    def get_object(self):
        return self.request.user

    def form_valid(self, form):
        form.instance.nurse = self.request.user
        return super().form_valid(form)

