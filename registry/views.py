from django.shortcuts import render
from django.http import HttpResponseRedirect
from cart.mixins import CartMixin
from django.views.generic import View
from categorys.models import Category
from registry.forms import RegistryForm
from django.contrib.auth import authenticate, login
from customer.models import Customer

class RegistryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = RegistryForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'registry.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistryForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        if form.is_valid():
            new_user_registered = form.save(commit=False)
            new_user_registered.username = form.cleaned_data['username']
            new_user_registered.email = form.cleaned_data['email']
            new_user_registered.first_name = form.cleaned_data['first_name']
            new_user_registered.last_name = form.cleaned_data['last_name']
            new_user_registered.phone_number = form.cleaned_data['phone_number']
            new_user_registered.save()
            new_user_registered.set_password(form.cleaned_data['password'])
            new_user_registered.save()
            Customer.objects.create(
                user=new_user_registered,
                phone_number=form.cleaned_data['phone_number'],
            )
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )
            login(request, user)
            return HttpResponseRedirect('/')
        return render(request, 'registry.html', context)
