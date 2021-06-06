from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import View

from categorys.models import Category
from cart.mixins import CartMixin
from login.forms import LoginForm


class LoginView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        categories = Category.objects.all()
        context = {'form': form, 'categories': categories, 'cart': self.cart}
        return render(request, 'login.html', context)
