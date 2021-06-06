from django.shortcuts import render
from django.http import HttpResponseRedirect
from customer.models import Customer
from order.forms import OrderForm
from django.db import transaction
from cart.mixins import CartMixin
from django.views.generic import View
from django.contrib import messages


class MakeOrderView(CartMixin, View):

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.delivery_type = form.cleaned_data['delivery_type']
            new_order.order_date = form.cleaned_data['order_date']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()
            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.orders.add(new_order)
            messages.add_message(request, messages.INFO,
                                 f'Благодарим за заказ, {new_order.first_name}! Заказ будет обработан в течение 30 минут')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')
