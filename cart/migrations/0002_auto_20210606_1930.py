# Generated by Django 3.1.1 on 2021-06-06 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cartproduct', '0001_initial'),
        ('cart', '0001_initial'),
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer', verbose_name='Владелец'),
        ),
        migrations.AddField(
            model_name='cart',
            name='products',
            field=models.ManyToManyField(blank=True, related_name='related_cart', to='cartproduct.CartProduct'),
        ),
    ]
