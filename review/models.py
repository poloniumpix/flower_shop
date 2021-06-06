from django.db import models


class Review(models.Model):

    def __str__(self):
        return str(self.id)
