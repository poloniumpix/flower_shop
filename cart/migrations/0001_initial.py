# Generated by Django 3.1.1 on 2021-06-06 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_products', models.PositiveIntegerField(default=0)),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=9, verbose_name='Общая цена:')),
                ('in_order', models.BooleanField(default=False)),
                ('for_anon_user', models.BooleanField(default=False)),
            ],
        ),
    ]
