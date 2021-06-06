from django.db import models
from django.urls import reverse
from categorys.models import Category
from customer.models import Customer


class Product(models.Model):
    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Стоимость')
    color = models.CharField(max_length=255, verbose_name='Окраска цветка:', default='Красная', null=True, blank=True)
    season = models.CharField(max_length=255, verbose_name='Сезон цветения:', default='Весна', null=True, blank=True)
    place = models.CharField(max_length=255, verbose_name='Размещение в квартире:', default='Тень', null=True,
                             blank=True)
    complectation = models.CharField(max_length=255, verbose_name='Комплектация:', default='Укорененный черенок',
                                     null=True, blank=True)

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    def get_absolute_url(self):
        return reverse('product_detail', kwargs={'slug': self.slug})


