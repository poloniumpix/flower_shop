from django.contrib import admin
from product.models import Product
from cart.models import Cart
from cartproduct.models import CartProduct
from categorys.models import Category
from customer.models import Customer
from order.models import Order


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)



