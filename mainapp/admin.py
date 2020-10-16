from django.forms import ModelChoiceField
from django.contrib import admin
from .models import *


class FuchsiaAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='fuchsia'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class VioletAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='violets'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class RoseAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='rose'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class GloxiniaAdmin(admin.ModelAdmin):

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            return ModelChoiceField(Category.objects.filter(slug='gloxinia'))
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Category)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Fuchsia, FuchsiaAdmin)
admin.site.register(Violet, VioletAdmin)
admin.site.register(Gloxinia, GloxiniaAdmin)
admin.site.register(Rose, RoseAdmin)


# Register your models here.
