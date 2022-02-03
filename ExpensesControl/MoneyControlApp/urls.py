from django.urls import path
from .views import *

urlpatterns = [
    path('operations/', Operations.as_view(), name='operations'),

    path('expense/add', AddExpense.as_view(), name='add_expense'),
    path('expense/<int:operation_id>/edit', EditExpense.as_view(), name='edit_expense'),

    path('operation/<int:operation_id>/delete', DeleteOperation.as_view(), name='delete_operation'),
]