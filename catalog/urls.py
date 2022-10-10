from django.urls import path
from django.views.decorators.cache import cache_page

from .views import *

app_name = 'catalog'

urlpatterns = [
    path('', cache_page(60 * 5)(HomeListView.as_view()), name='home'),
    path('go-shopping/<int:pk>/', redirect_to_admitad, name='redirect_to_admitad'),
    path('category/<str:slug>/', cache_page(60 * 5)(ProductsByCategory.as_view()), name='get_categories'),
    path('search/', Search.as_view(), name='search'),
]
