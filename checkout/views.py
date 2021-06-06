from django.shortcuts import render
from cart.mixins import CartMixin
from django.views.generic import View
from categorys.models import Category
from order.forms import OrderForm

class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'categories': categories,
            'form': form
        }
        return render(request, 'order_checkout.html', context)
