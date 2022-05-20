from django.db import models

from products.models import Product


class Cart(models.Model):
    is_editable = models.BooleanField(default=True, null=False)
    products = models.ManyToManyField(Product, through="CartProduct")


class CartProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField(default=0, null=True)
    price = models.PositiveIntegerField(default=0, null=True)
    count = models.PositiveIntegerField(default=0, null=False)

    class Meta:
        unique_together = ("product", "cart")
