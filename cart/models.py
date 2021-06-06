from django.db import models



class Cart(models.Model):
    owner = models.ForeignKey('customer.Customer', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField('cartproduct.CartProduct', blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(default=0, max_digits=9, decimal_places=2, verbose_name='Общая цена:')
    in_order = models.BooleanField(default=False)
    for_anon_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


