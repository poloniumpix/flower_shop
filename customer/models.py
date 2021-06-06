from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

class Customer(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone_number = models.CharField(null=True, blank=True, max_length=20, verbose_name='Номер телефона:')
    address = models.CharField(null=True, blank=True, max_length=255, verbose_name='Адрес:')
    orders = models.ManyToManyField('order.Order', verbose_name='Оформленные заказы', related_name='related_customer')

    def __str__(self):
        return f"Покупатель: {self.user.first_name} {self.user.last_name}"
