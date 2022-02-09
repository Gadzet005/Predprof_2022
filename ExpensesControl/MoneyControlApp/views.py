from django.contrib.auth.mixins import LoginRequiredMixin
from django.http.response import HttpResponse
from django_filters.views import FilterView
from django.contrib import messages
from django.urls.base import reverse_lazy
from django.views.generic import *
from openpyxl import Workbook

from .models import *
from .filters import *
from MainApp.models import *
from .forms import *


class Operations(LoginRequiredMixin, FilterView):
    template_name = "MoneyControlApp/operations.html"
    model = Operation
    login_url = reverse_lazy("login")
    filterset_class = OperationsFilter

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Операции"
        return context

    def get_queryset(self):
        # Показывает пользователю только его изменения баланса
        return Operation.objects.filter(user=self.request.user)

class AddOperation(LoginRequiredMixin, CreateView):
    form_class = OperationForm
    template_name = 'MainApp/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('operations')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Добавить операцию"
        context["h3_text"] = "Добавить операцию"
        context["button_text"] = "Добавить"
        return context
    
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно добавили операцию.')
        return super().form_valid(form)

class EditOperation(LoginRequiredMixin, UpdateView):
    model = Operation
    form_class = OperationForm
    pk_url_kwarg = "operation_id"
    template_name = 'MainApp/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('operations')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменить операцию"
        context["h3_text"] = "Изменить операцию"
        context["button_text"] = "Сохранить"
        return context

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, 'Вы успешно изменили операцию.')
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

class Categories(LoginRequiredMixin, ListView):
    template_name = "MoneyControlApp/categories.html"
    model = Category
    context_object_name = "categories"
    login_url = reverse_lazy("login")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Категории"
        return context

class ExportData(LoginRequiredMixin, FormView):
    model = Operation
    form_class = ExportDataForm
    template_name = 'MainApp/form.html'
    login_url = reverse_lazy('login')
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Экспорт данных"
        context["h3_text"] = "Перевод данных в .xlsx"
        context["button_text"] = "Скачать"
        return context

    def form_valid(self, form):
        # Получаем данные из формы и сортируем операции
        date = form.cleaned_data['date']
        operations = OperationsFilter.date_filter(Operation.objects, None, date).filter(user=self.request.user)
        
        TABLE_HEAD = ["Тип", "Сумма", "Дата", "Категория"]

        # Создаем таблицу
        workbook = Workbook()
        sheet = workbook.active

        # Создаем шапку таблицы
        for col, val in enumerate(TABLE_HEAD):
            sheet.cell(row=1, column=col + 1, value=val)
        
        # Вставляем данные в таблицу
        for row, operation in enumerate(operations):
            values = [operation.category.type, operation.amount, operation.date, operation.category.name]
            for col, val in enumerate(values):
                sheet.cell(row=row + 2, column=col + 1, value=val)
        
        # Подготовка файла для передачи пользователю
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=operations.xlsx'
        workbook.save(response)

        return response