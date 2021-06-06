from django.shortcuts import render
from cart.mixins import CartMixin
from django.views.generic import View
from categorys.models import Category


class DeliveryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'delivery.html', context)
