from cart.mixins import CartMixin
from categorys.models import Category
from product.models import Product
from django.views.generic import DetailView


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
