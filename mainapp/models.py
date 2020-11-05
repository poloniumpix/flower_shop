from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse
from django.utils import timezone

from .managers import CategoryManager, FuchsiaManager, VioletManager, RoseManager, GloxiniaManager


User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:7]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(
                        products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
                    )
        return products


class LatestProducts:

    objects = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Стоимость')
    specie = models.CharField(max_length=255, verbose_name='Вид растения', null=True, blank=True)

    class Meta:
        abstract = True

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

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name='Общая цена:')
    in_order = models.BooleanField(default=False)
    for_anon_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(null=True, blank=True, max_length=20, verbose_name='Номер телефона:')
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name='Адрес:')
    orders = models.ManyToManyField('Order', verbose_name='Оформленные заказы', related_name='related_customer')


    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"


class Flower(Product):

    color = models.CharField(max_length=255, verbose_name='Окраска цветка:', default='Красная', null=True, blank=True)
    season = models.CharField(max_length=255, verbose_name='Сезон цветения:', default='Весна', null=True, blank=True)
    place = models.CharField(max_length=255, verbose_name='Размещение в квартире:', default='Тень', null=True, blank=True)
    complectation = models.CharField(max_length=255, verbose_name='Комплектация:', default='Укорененный черенок', null=True, blank=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Fuchsia(Flower):

    objects = FuchsiaManager()

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Violet(Flower):

    objects = VioletManager()

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Gloxinia(Flower):

    objects =GloxiniaManager()

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Rose(Flower):

    objects = RoseManager()

    def __str__(self):
        return f"{self.category.name} : {self.title}"

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'ready'
    STATUS_COMPLETED = 'completed'

    DELIVERY_TYPE_PICKUP = 'pickup'
    DELIVERY_TYPE_COURIER = 'delivery'

    STATUS_CHOICE = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов к доставке'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    DELIVERY_TYPE_CHOICE = (
        (DELIVERY_TYPE_PICKUP, 'Самовывоз'),
        (DELIVERY_TYPE_COURIER, 'Доставка курьером')
    )

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=1024, verbose_name='Адрес', null=True, blank=True)
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')
    order_date = models.DateField(verbose_name='Дата получения заказа', default=timezone.now)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказа',
        choices=STATUS_CHOICE,
        default=STATUS_NEW
    )
    delivery_type = models.CharField(
        max_length=100,
        verbose_name='Тип доставки',
        choices=DELIVERY_TYPE_CHOICE,
        default=DELIVERY_TYPE_PICKUP
    )

    def __str__(self):
        return str(self.id)


class Comment(models.Model):

    def __str__(self):
        return str(self.id)




















