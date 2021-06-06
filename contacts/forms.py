from django import forms

from mainapp.models import Comment


class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=500, label="Имя")
    email = forms.EmailField(max_length=500, label="Еmail-адрес")
    comment = forms.CharField(label='', widget=forms.Textarea(
        attrs={'placeholder': 'Введите ваше сообщение'}))

    class Meta:
        model = Comment
        fields = ('name', 'email', 'comment')