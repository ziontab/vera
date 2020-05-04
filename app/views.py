import datetime

from django import forms
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.contrib.auth import login
from django.contrib.auth.views import LoginView as ContribLoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from app import models, forms as app_forms


class IndexView(TemplateView):
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

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)
        form.fields['first_name'].widget = forms.TextInput(attrs={'placeholder': 'Имя подопечного'})
        form.fields['middle_name'].widget = forms.TextInput(attrs={'placeholder': 'Отчество подопечного'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'placeholder': 'Фамилия подопечного'})
        form.fields['birthday'].widget = forms.TextInput(attrs={'placeholder': 'Дата рождения ГГГГ-ММ-ДД'})
        form.fields['address'].widget = forms.TextInput(attrs={'placeholder': 'Адрес'})
        form.fields['phone'].widget = forms.TextInput(attrs={'placeholder': 'Телефон'})
        return form

    def form_valid(self, form):
        form.instance.nurse = self.request.user
        response = super().form_valid(form)
        models.Event.objects.create(
            nurse=self.request.user,
            ward=self.object,
            date_planned=datetime.datetime.now(),
            title='Гигиена лица и полости рта',
        )
        models.Event.objects.create(
            nurse=self.request.user,
            ward=self.object,
            date_planned=datetime.datetime.now(),
            title='Приём лекарства',
        )
        models.Event.objects.create(
            nurse=self.request.user,
            ward=self.object,
            date_planned=datetime.datetime.now() + datetime.timedelta(days=1),
            title='Приём пищи',
        )
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diseases'] = models.Disease.objects.all()
        return context


class EventsView(LoginRequiredMixin, TemplateView):
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['events'] = models.Event.objects.filter(
            nurse=self.request.user,
            date_planned__gte=datetime.date.today(),
            date_planned__lte=datetime.date.today() + datetime.timedelta(days=1),
            is_complete=False,
        ).order_by('date_planned')
        context['today'] = datetime.date.today().strftime('%D')
        context['days'] = create_days()
        return context

class EventsByDateView(LoginRequiredMixin, TemplateView):
    template_name = "events.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = self.kwargs.get('date').split('-')
        date = datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))
        context['events'] = models.Event.objects.filter(
            nurse=self.request.user,
            date_planned__gte=date,
            date_planned__lte=date + datetime.timedelta(days=1),
            is_complete=False,
        ).order_by('date_planned')
        context['today'] = datetime.date.today().strftime('%D')
        context['days'] = create_days(date)
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
    paginate_by = 3

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

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super().get_form(form_class)
        form.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Логин'})
        form.fields['password'].widget = forms.PasswordInput(attrs={'placeholder': 'Пароль'})
        return form


class SignupView(FormView):
    template_name = "signup.html"
    form_class = app_forms.SignupForm
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


@require_POST
def event_complete(request):
    event = models.Event.objects.filter(
        pk=request.POST.get('id'),
        nurse=request.user,
    ).first()
    if event:
        event.date_close = datetime.datetime.now()
        event.is_complete = True
        event.save()
    return JsonResponse({"status": "ok"})


@require_POST
def articles_like(request):
    article = models.Article.objects.filter(
        pk=request.POST.get('id'),
    ).first()
    if article:
        models.Like.objects.get_or_create(nurse=request.user, article=article)
    return JsonResponse({"status": "ok"})


def create_days(date=None):
    if not date:
        date = datetime.date.today()
    start = datetime.date.today()
    result = []
    for x in range(7):
        result.append({
            "date": start.isoformat(),
            "name": start.strftime('%a'),
            "active": True if start == date else False,
            "number": start.day,
        })
        start = start + datetime.timedelta(days=1)
    return result


