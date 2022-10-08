from django.urls import include, path

from .views import *

app_name = 'catalog'

urlpatterns = [
    path('', HomeListView.as_view(), name='home'),
    path('go-shopping/<int:pk>/', redirect_to_admitad, name='redirect_to_admitad'),
    path('category/<str:slug>/', ProductsByCategory.as_view(), name='get_categories'),
]
