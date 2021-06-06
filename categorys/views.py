from django.shortcuts import render
from categorys.models import Category
from cart.mixins import CartMixin
from django.views.generic import DetailView


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

