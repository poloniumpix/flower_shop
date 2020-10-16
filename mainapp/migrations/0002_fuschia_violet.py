# Generated by Django 3.1.2 on 2020-10-12 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Violet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение:')),
                ('description', models.TextField(null=True, verbose_name='Описание:')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Стоимость:')),
                ('sort', models.CharField(max_length=255, verbose_name='Сорт:')),
                ('color', models.CharField(max_length=255, verbose_name='Окраска цветка:')),
                ('season', models.CharField(max_length=255, verbose_name='Сезон цветения:')),
                ('place', models.CharField(max_length=255, verbose_name='Благоприятное расположение в квартире:')),
                ('complectation', models.CharField(max_length=255, verbose_name='Комплектация:')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fuschia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Наименование')),
                ('slug', models.SlugField(unique=True)),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение:')),
                ('description', models.TextField(null=True, verbose_name='Описание:')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Стоимость:')),
                ('sort', models.CharField(max_length=255, verbose_name='Сорт:')),
                ('color', models.CharField(max_length=255, verbose_name='Окраска цветка:')),
                ('season', models.CharField(max_length=255, verbose_name='Сезон цветения:')),
                ('place', models.CharField(max_length=255, verbose_name='Благоприятное расположение в квартире:')),
                ('complectation', models.CharField(max_length=255, verbose_name='Комплектация:')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.category', verbose_name='Категория')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
