from django.urls import path
from .views import *

urlpatterns = [
    path('operations', Operations.as_view(), name='operations'),
    path('operation/add', AddOperation.as_view(), name='add_operation'),
    path('operation/<int:operation_id>/edit', EditOperation.as_view(), name='edit_operation'),
    path('operation/<int:operation_id>/delete', DeleteOperation.as_view(), name='delete_operation'),

    path('export_data/', ExportData.as_view(), name='export_data'),

    path('categories/', Categories.as_view(), name='categories'),
]