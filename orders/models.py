from django.db import models

from carts.models import Cart

from .enums import OrderStatusEnum


class Order(models.Model):
    status = models.CharField(
        max_length=20,
        choices=OrderStatusEnum.choices,
        default=OrderStatusEnum.PROCESSING,
    )
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE, unique=True)
    name = models.CharField(max_length=200, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
