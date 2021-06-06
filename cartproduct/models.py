from django.db import models
from product.models import Product


class CartProduct(models.Model):
    user = models.ForeignKey('customer.Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('cart.Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    product = models.ForeignKey(Product, verbose_name='Товар', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена:')

    def __str__(self):
        return f'Продукт: {self.product.title} (для корзины)'

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.product.price
        super().save(*args, **kwargs)
