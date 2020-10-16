from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse


User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Фуксии': 'fuchsia__count',
        'Фиалки': 'violet__count',
        'Глоксинии': 'gloxinia__count',
        'Розы': 'rose__count',

    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('fuchsia', 'rose', 'gloxinia', 'violet')
        qs = list(self.get_queryset().annotate(*models).values())
        return [dict(name=c['name'], slug=c['slug'], count=c[self.CATEGORY_NAME_COUNT_NAME[c['name']]]) for c in qs]


class Category(models.Model):

    name = models.CharField(max_length = 255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение:')
    description = models.TextField(verbose_name='Описание:', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Стоимость:')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена:')

    def __str__(self):
        return f'Продукт: {self.content_object.title} (для корзины)'


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, verbose_name='Общая цена:')
    in_order = models.BooleanField(default=False)
    for_anon_user = models.BooleanField(default=False)

    def __str__(self):
        return self.id


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефона:')
    address = models.CharField(max_length=255, verbose_name='Адрес:')


    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Flower(Product):

    class Meta:
        abstract = True

    # sort = models.CharField(max_length=255, verbose_name='Сорт:')
    color = models.CharField(max_length=255, verbose_name='Окраска цветка:')
    season = models.CharField(max_length=255, verbose_name='Сезон цветения:')
    place = models.CharField(max_length=255, verbose_name='Размещение в квартире:')
    complectation = models.CharField(max_length=255, verbose_name='Комплектация:')


class Fuchsia(Flower):

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Violet(Flower):

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Gloxinia(Flower):

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Rose(Flower):

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')














