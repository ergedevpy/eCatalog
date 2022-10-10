from django.shortcuts import redirect
from django.views.generic import ListView
from django.db.models import Q
from django.shortcuts import render

from .models import Product, Category


def redirect_to_admitad(request, pk):
    redirect_url = Product.objects.filter(pk=pk).values_list('redirect_url').first()

    return redirect(redirect_url[0], )


class HomeListView(ListView):
    queryset = Product.objects.select_related('category').order_by('vendor').all()[:8]
    paginate_by = 8
    template_name = 'catalog/home.html'


class ProductsByCategory(ListView):
    template_name = 'catalog/category.html'
    context_object_name = 'category'
    paginate_by = 12
    allow_empty = False

    def get_queryset(self):
        return Product.objects.select_related('category').filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        self.context_data = super().get_context_data(**kwargs)
        self.data = self.context_data
        context = self.data
        context['title'] = f'Категорія: {Category.objects.get(slug=self.kwargs["slug"])} | ERGE.ONE'
        context['category_name'] = Category.objects.get(slug=self.kwargs["slug"])
        return context


class Search(ListView):
    template_name = 'catalog/search.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.select_related('category').filter(Q(name__icontains=self.request.GET.get('s')) |
                                                                 Q(description__icontains=self.request.GET.get('s')) |
                                                                 Q(code__icontains=self.request.GET.get('s')) |
                                                                 Q(vendor__name__icontains=self.request.GET.get('s')))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Результат пошуку для: {self.request.GET.get("s")}'
        context['s'] = f's={self.request.GET.get("s")}&'
        return context


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)

