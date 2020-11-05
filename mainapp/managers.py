from django.db import models
from django.db.models import Q


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME = {
        'Фуксии': 'fuchsia__count',
        'Фиалки': 'violet__count',
        'Глоксинии': 'gloxinia__count',
        'Розы': 'rose__count',

    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('fuchsia', 'rose', 'gloxinia', 'violet')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class FuchsiaManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(specie__icontains=query) | Q(color__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class GloxiniaManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(specie__icontains=query) | Q(color__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class RoseManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(specie__icontains=query) | Q(color__icontains=query))
            qs = qs.filter(or_lookup)

        return qs


class VioletManager(models.Manager):
    use_for_related_fields = True

    def search(self, query=None):
        qs = self.get_queryset()
        if query:
            or_lookup = (Q(specie__icontains=query) | Q(color__icontains=query))
            qs = qs.filter(or_lookup)

        return qs

