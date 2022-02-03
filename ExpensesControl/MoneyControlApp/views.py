from django.contrib.auth.mixins import LoginRequiredMixin 
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.views.generic import *

from .models import *
from .forms import *

class Operations(LoginRequiredMixin, ListView):
    template_name = "MoneyControlApp/list.html"
    model = Operation
    context_object_name = "operations"
    login_url = reverse_lazy("login")

    def __init__(self):
        self.filter = None
        self.sort = None
        super().__init__()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Операции"
        return context

    def get_queryset(self):
        # Показывает пользователю только его изменения баланса
        return Operation.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        if "filter" in  kwargs:
            self.filter = kwargs["filter"]
        if "sort" in kwargs:
            self.sort = kwargs["sort"]
        return super().get(request, *args, **kwargs)

class AddExpense(LoginRequiredMixin, CreateView):
    form_class = OperationForm
    template_name = 'MainApp/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('operations')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить расход"
        context["button_text"] = "Добавить"
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно добавили расход.')
        return super().form_valid(form)

class EditExpense(LoginRequiredMixin, UpdateView):
    model = Operation
    form_class = OperationForm
    pk_url_kwarg = "operation_id"
    template_name = 'MainApp/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('operations')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить расход"
        context["h3_text"] = "Изменить расход"
        context["button_text"] = "Сохранить"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно изменили параметры расхода.')
        return super().form_valid(form)
    
    def get_queryset(self):
        # Пользователь может изменять только свои расходы
        return Operation.objects.filter(user=self.request.user)

class DeleteOperation(LoginRequiredMixin, DeleteView):
    model = Operation
    template_name = 'MainApp/form.html'
    pk_url_kwarg = "operation_id"
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('operations')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Удалить операцию"
        context["h3_text"] = "Удалить операцию"
        context["button_text"] = "Да"
        context["text"] = "Вы точно хотите операцию?"
        return context

    def post(self, request, *args, **kwargs):
        messages.add_message(request, messages.SUCCESS, 'Вы успешно удалили операцию.')
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        # Пользователь может удалять только свои операции
        return Operation.objects.filter(user=self.request.user)
