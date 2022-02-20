from codecs import register
from sqlite3 import register_converter
from django.contrib import admin
from .models import *

admin.site.register(Category)
admin.site.register(Variable)
