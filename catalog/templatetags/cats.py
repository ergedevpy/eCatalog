from django import template
from catalog.models import Category
from django.db.models import Count

register = template.Library()


@register.inclusion_tag('catalog/cats_tpl.html')
def show_cats():
    categories = Category.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    return {'categories': categories}


@register.inclusion_tag('catalog/cats_menu_tpl.html')
def show_menu_cats():
    categories = Category.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    return {'categories': categories}
