from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, ListView
from django.core.mail import send_mail
from django.db.models import Q

from .models import Category, Customer, CartProduct, Product, Order
from .mixins import CartMixin
from .forms import OrderForm, ContactForm, LoginForm, RegistryForm
from .utilities import recalc_cart


class BasicView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()
        context = {'categories': categories,
                   'products': products,
                   'cart': self.cart}
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, DetailView):
    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['cart'] = self.cart
        context['categories'] = categories
        return context


class CategoryDetailView(CartMixin, DetailView):
    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        context['cart'] = self.cart
        context['categories'] = categories
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, product=product
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен в корзину")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален из корзины")
        return HttpResponseRedirect('/cart/')


class ChangeQuantityView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        product_slug = kwargs.get('slug')
        product = Product.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Количество успешно изменено")
        return HttpResponseRedirect('/cart/')


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
                                 f'Благодарим за заказ, {new_order.first_name}! Заказ будет обработан в течение 20 минут')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class ContactsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        categories = Category.objects.all()
        context = {'cart': self.cart,
                   'categories': categories,
                   'form': form}
        return render(request, 'contacts.html', context)

    @transaction.atomic
    def post(self, request):
        categories = Category.objects.all()
        name = ''
        email = ''
        comment = ''
        form = ContactForm(request.POST or None)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            email = form.cleaned_data.get("email")
            comment = form.cleaned_data.get("comment")
            subject = "Пользовательское обращение (Florus)"
            comment = f"Пользователь {name} с e-mail адресом {email} отправил сообщение:\n\n {comment}"
            send_mail(subject, comment, 'florus.service@gmail.com', [email])
            messages.add_message(request, messages.INFO,
                                 f'Благодарим за обращение! Оно будет рассмотрено в течение 2 часов')
            return HttpResponseRedirect('/')

        else:
            context = {'form': form,
                       'cart': self.cart,
                       'categories': categories}
            return render(request, 'contacts.html', context)


class DeliveryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'delivery.html', context)


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


class CustomerAccountView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-created_at')
        context = {'categories': categories, 'cart': self.cart, 'orders': orders}
        return render(request, 'customer_account.html', context)


class SearchResultView(CartMixin, ListView):
    model = Product
    template_name = 'search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(color__icontains=query)
        )
        return object_list