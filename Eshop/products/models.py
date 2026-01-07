from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=500)
    price =models.PositiveIntegerField()
    stock =models.PositiveIntegerField()
    thumbnail =models.ImageField(upload_to='products/thumbnails/')