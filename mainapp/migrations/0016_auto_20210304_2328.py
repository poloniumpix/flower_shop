# Generated by Django 3.1.1 on 2021-03-04 20:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0015_auto_20201105_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Стоимость')),
                ('specie', models.CharField(blank=True, max_length=255, null=True, verbose_name='Вид растения')),
                ('color', models.CharField(blank=True, default='Красная', max_length=255, null=True, verbose_name='Окраска цветка:')),
                ('season', models.CharField(blank=True, default='Весна', max_length=255, null=True, verbose_name='Сезон цветения:')),
                ('place', models.CharField(blank=True, default='Тень', max_length=255, null=True, verbose_name='Размещение в квартире:')),
                ('complectation', models.CharField(blank=True, default='Укорененный черенок', max_length=255, null=True, verbose_name='Комплектация:')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
        ),
        migrations.RemoveField(
            model_name='gloxinia',
            name='category',
        ),
        migrations.RemoveField(
            model_name='rose',
            name='category',
        ),
        migrations.RemoveField(
            model_name='violet',
            name='category',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='cartproduct',
            name='object_id',
        ),
        migrations.DeleteModel(
            name='Fuchsia',
        ),
        migrations.DeleteModel(
            name='Gloxinia',
        ),
        migrations.DeleteModel(
            name='Rose',
        ),
        migrations.DeleteModel(
            name='Violet',
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='mainapp.product', verbose_name='Товар'),
            preserve_default=False,
        ),
    ]