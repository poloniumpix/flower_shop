from django import forms
from django.contrib.auth.models import User

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


class RegistryForm(forms.ModelForm):
    password_confirm = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(required=False)
    email = forms.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['password_confirm'].label = 'Подтвердите пароль'
        self.fields['email'].label = 'Е-mail'
        self.fields['phone_number'].label = 'Номер телефона'
        self.fields['first_name'].label = 'Имя'
        self.fields['last_name'].label = 'Фамилия'

    def clean_email(self):
        email = self.cleaned_data['email']
        if '@' not in email:
            raise forms.ValidationError('Введите корректный е-mail адрес!')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким e-mail адресом уже существует!')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким никнеймом уже существует!')
        return username

    def clean(self):
        password = self.cleaned_data['password']
        password_confirm = self.cleaned_data['password_confirm']
        if password != password_confirm:
            raise forms.ValidationError('Введенные пароли не совпадают!')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'phone_number']


class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        if not User.objects.filter(username=username).exists:
            raise forms.ValidationError(f'Пользователь с логином {username} не найден')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Введен неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']
