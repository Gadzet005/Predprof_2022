from django import template
from MainApp.models import Category

register = template.Library()

@register.simple_tag()
def get_cat_type():
    return {cat.id: cat.type for cat in Category.objects.all()}