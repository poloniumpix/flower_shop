from django import forms

from .models import Order, Comment


class OrderForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['order_date'].label = 'Дата доставки'

    order_date = forms.DateField(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'phone', 'address', 'delivery_type', 'order_date', 'comment')


class ContactForm(forms.ModelForm):

    name = forms.CharField(max_length=500, label="Имя")
    email = forms.EmailField(max_length=500, label="Еmail-адрес")
    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Введите ваше сообщение'}))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')


