from unidecode import unidecode
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Merchant(models.Model):
    name = models.CharField(max_length=255, verbose_name='Продавець')
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    logo_url = models.CharField(max_length=512, verbose_name='Лого', blank=True, null=True)
    site = models.URLField(verbose_name='Сайт', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Merchant, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Merchant'
        verbose_name_plural = 'Merchants'
        ordering = ['name']


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True, verbose_name='Категорія')
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    parent_cat = models.ForeignKey('Category', verbose_name='Батьківська категорія', on_delete=models.CASCADE,
                                   blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('catalog:get_categories', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']


class Vendor(models.Model):
    name = models.CharField(max_length=64, default='Невідомо', verbose_name='Виробник', db_index=True, unique=True)
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    logo_url = models.CharField(max_length=512, verbose_name='Лого', blank=True, null=True)
    site = models.URLField(verbose_name='Сайт', blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Vendor, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Vendor'
        verbose_name_plural = 'Vendors'
        ordering = ['name']


class Product(models.Model):
    prod_id = models.CharField(max_length=12, verbose_name='Ідентифікатор продавця')
    code = models.CharField(max_length=50, verbose_name='Код продавця')
    name = models.CharField(max_length=512, db_index=True, verbose_name='Найменування')
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)
    description = models.TextField(blank=True, null=True, verbose_name='Опис', db_index=True)
    picture = models.CharField(max_length=512, blank=True, null=True, verbose_name='Картинка')
    guarantee = models.CharField(max_length=255, blank=True, null=True, verbose_name='Гарантія')
    stock = models.CharField(max_length=255, blank=True, null=True, verbose_name='Наявність')
    oldprice = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Стара ціна')
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name='Ціна')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='Продавець')
    vendor = models.ForeignKey(Vendor, blank=True, null=True, on_delete=models.CASCADE, verbose_name='Виробник')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія')
    redirect_url = models.URLField(verbose_name='Посилання на товар')

    def __str__(self):
        return self.name

    def get_discount_percent(self):
        if self.oldprice and self.price:
            discount_percent = 100 - ((self.price * 100) / self.oldprice)
            return discount_percent

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.name))
        super(Product, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        ordering = ['-id']
