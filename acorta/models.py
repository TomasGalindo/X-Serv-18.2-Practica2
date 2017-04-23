from django.db import models
# Create your models here.


class URL(models.Model):
    name = models.URLField()
