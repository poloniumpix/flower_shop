from django.db import transaction
from itertools import chain
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, View, ListView
from django.core.mail import send_mail

from .models import Fuchsia, Gloxinia, Rose, Violet, Category, LatestProducts, Customer, Cart, CartProduct, Product, Flower
from .mixins import CategoryDetailMixin, CartMixin
from .forms import OrderForm, ContactForm
from .utilities import recalc_cart


class BasicView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        products = LatestProducts.objects.get_products_for_main_page('fuchsia', 'rose', 'violet', 'gloxinia')
        context = {'categories': categories,
                   'products': products,
                   'cart': self.cart}
        return render(request, 'base.html', context)


class ProductDetailView(CartMixin, CategoryDetailMixin, DetailView):

    CT_MODEL_CLASS = {
        'gloxinia': Gloxinia,
        'fuchsia': Fuchsia,
        'violet': Violet,
        'rose': Rose
    }

    def dispatch(self, request, *args, **kwargs):

        self.model = self.CT_MODEL_CLASS[kwargs['ct_model']]
        self.queryset = self.model._base_manager.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ct_model'] = self.model._meta.model_name
        context['cart'] = self.cart
        return context


class CategoryDetailView(CartMixin, CategoryDetailMixin, DetailView):

    model = Category
    queryset = Category.objects.all()
    context_object_name = 'category'
    template_name = 'category_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = self.cart
        return context


class CartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'cart.html', context)


class AddToCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        if created:
            self.cart.products.add(cart_product)
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно добавлен в корзину")
        return HttpResponseRedirect('/cart/')


class DeleteFromCartView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Товар успешно удален из корзины")
        return HttpResponseRedirect('/cart/')



class ChangeQuantityView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        ct_model, product_slug = kwargs.get('ct_model'), kwargs.get('slug')
        content_type = ContentType.objects.get(model=ct_model)
        product = content_type.model_class().objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, content_type=content_type, object_id=product.id
        )
        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        messages.add_message(request, messages.INFO, "Количество успешно изменено")
        return HttpResponseRedirect('/cart/')


class CheckoutView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
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
            messages.add_message(request, messages.INFO, f'Благодарим за заказ, {new_order.first_name}! Заказ будет обработан в течение 20 минут')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')


class ContactsView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {'cart': self.cart,
                   'categories': categories,
                   'form': form}
        return render(request, 'contacts.html', context)

    @transaction.atomic
    def post(self, request):
        categories = Category.objects.get_categories_for_left_sidebar()
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
            context = {'form': form,
                       'cart': self.cart,
                       'categories': categories
                       }
            messages.add_message(request, messages.INFO, f'Благодарим за обращение! Оно будет рассмотрено в течение 2 часов')
            return HttpResponseRedirect('/')

        else:
            context = {'form': form,
                       'cart': self.cart,
                       'categories': categories}
            return render(request, 'contacts.html', context)


class DeliveryView(CartMixin, View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {
            'cart': self.cart,
            'categories': categories
        }
        return render(request, 'delivery.html', context)


class SearchResultsView(CartMixin, View):

    template_name = 'search_results.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.get_categories_for_left_sidebar()
        context = {}

        q = request.GET.get('q')
        if q:
            query_sets = []
            query_sets.append(Fuchsia.objects.search(query=q))
            query_sets.append(Gloxinia.objects.search(query=q))
            query_sets.append(Rose.objects.search(query=q))
            query_sets.append(Violet.objects.search(query=q))

            final_set = list(chain(*query_sets))
            final_set.sort(key=lambda x: x.price, reverse=True)

            context['last_question'] = '?q=%s' % q

            current_page = Paginator(final_set, 10)

            page = request.GET.get('page')
            try:
                context['object_list'] = current_page.page(page)
            except PageNotAnInteger:
                context['object_list'] = current_page.page(1)
            except EmptyPage:
                context['object_list'] = current_page.page(current_page.num_pages)

        return render(request, template_name='search_results.html', context=context)



















