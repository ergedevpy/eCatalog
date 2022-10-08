from django import template
from django.db.models import Count

from catalog.models import Category

register = template.Library()


@register.inclusion_tag('catalog/cats_tpl.html')
def show_cats():
    categories = Category.objects.annotate(cnt=Count('product')).filter(cnt__gt=0)
    return {'categories': categories}
