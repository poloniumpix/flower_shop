from django.shortcuts import render
from django.views.generic import View

from categorys.models import Category
from product.models import Product
from cart.mixins import CartMixin


class BasicView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {'categories': categories,
                   'products': products,
                   'cart': self.cart}
        return render(request, 'base.html', context)



