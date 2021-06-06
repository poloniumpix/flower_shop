from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from cart.models import Cart

class Comment(models.Model):

    def __str__(self):
        return str(self.id)
