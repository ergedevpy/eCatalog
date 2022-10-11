from django.urls import path
from django.views.decorators.cache import cache_page

from .views import HomeListView, ProductsByCategory, Search, ProductDetailView, redirect_to_admitad

app_name = 'catalog'

urlpatterns = [
    path('go-shopping/<int:pk>/', redirect_to_admitad, name='redirect_to_admitad'),
    # path('', cache_page(60 * 5)(HomeListView.as_view()), name='home'),
    # path('category/<str:slug>/', cache_page(60 * 5)(ProductsByCategory.as_view()), name='get_categories'),
    path('', HomeListView.as_view(), name='home'),
    path('category/<str:slug>/', ProductsByCategory.as_view(), name='get_categories'),
    path('product/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('search/', Search.as_view(), name='search'),
]
