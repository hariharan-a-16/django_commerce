from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField(max_length=500)
    price =models.PositiveIntegerField()
    stock =models.PositiveIntegerField()
    thumbnail =models.ImageField(upload_to='products/thumbnails/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    img = models.ImageField(upload_to = 'products/images/')
    caption = models.CharField(max_length=200, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.title} image"