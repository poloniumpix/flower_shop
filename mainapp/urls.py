from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    BasicView,
    ProductDetailView,
    CategoryDetailView,
    CartView,
    AddToCartView,
    DeleteFromCartView,
    ChangeQuantityView,
    CheckoutView,
    MakeOrderView,
    ContactsView,
    DeliveryView,
    RegistryView,
    LoginView,
    CustomerAccountView,
    SearchResultView
)

urlpatterns = [
    path('', BasicView.as_view(), name='base'),
    path('products/<str:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('category/<str:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('remove-from-cart/<str:slug>/', DeleteFromCartView.as_view(), name='delete_from_cart'),
    path('change-qty/<str:slug>/', ChangeQuantityView.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/', MakeOrderView.as_view(), name='make_order'),
    path('contacts/', ContactsView.as_view(), name='contacts'),
    path('delivery/', DeliveryView.as_view(), name='delivery'),
    path('registry/', RegistryView.as_view(), name='registry'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('account/', CustomerAccountView.as_view(), name='account'),
    path('search_results/', SearchResultView.as_view(), name='search_results')
]
