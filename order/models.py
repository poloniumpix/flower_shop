from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from customer.models import Customer
from cart.models import Cart


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

    customer = models.ForeignKey(Customer, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE)
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
