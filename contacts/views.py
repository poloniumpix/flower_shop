from django.db import transaction
from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import View
from django.core.mail import send_mail

from categorys.models import Category
from cart.mixins import CartMixin
from contacts.forms import ContactForm

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
