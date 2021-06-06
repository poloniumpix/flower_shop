from django.shortcuts import render
from cart.mixins import CartMixin
from django.views.generic import DetailView, View, ListView
from order.models import Order
from categorys.models import Category
from customer.models import Customer

class CustomerAccountView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        context = {'categories': categories, 'cart': self.cart, 'orders': orders}
        return render(request, 'customer_account.html', context)

