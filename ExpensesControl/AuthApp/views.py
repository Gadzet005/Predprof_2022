from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout, login
from django.urls.base import reverse_lazy

from .forms import *

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'MainApp/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Регистрация'
        context["button_text"] = "Зарегистрироваться"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно создали аккаунт')
        user = form.save()
        login(self.request, user)
        return redirect('home')

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'MainApp/form.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Вход"
        context["button_text"] = "Войти"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, f'С возвращением {form.cleaned_data["username"]}!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')

class EditUserData(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ChangeUserDataForm
    template_name = 'MainApp/form.html'
    success_url = reverse_lazy('home')
    login_url = reverse_lazy('login')

    def get_object(self):
        return self.request.user

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактировать данные"
        context["button_text"] = "Сохранить"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно изменили пользовательские данные.')
        return super().form_valid(form)

class ChangePassword(LoginRequiredMixin, PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'MainApp/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить пароль"
        context["button_text"] = "Изменить"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно изменили пароль.')
        return super().form_valid(form)

def logout_user(request):
    logout(request)
    return redirect('login')
