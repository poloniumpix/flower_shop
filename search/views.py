from django.shortcuts import render
from cart.mixins import CartMixin
from categorys.models import Category
from product.models import Product
from django.views.generic import View
from django.db.models import Q


class SearchResultView(CartMixin, View):
    model = Product
    template_name = 'search_results.html'

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        categories = Category.objects.all()
        object_list = Product.objects.filter(
            Q(title__icontains=query) | Q(color__icontains=query)
        )
        context = {'categories': categories, 'cart': self.cart, 'object_list': object_list}
        return render(request, 'search_results.html', context)
