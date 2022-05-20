from django.db import models

from .enums import ProductStatusEnum


class Product(models.Model):
    title = models.CharField(max_length=200, null=False)
    cost = models.PositiveIntegerField(default=0, null=False)
    price = models.PositiveIntegerField(default=0, null=False)
    stock = models.PositiveIntegerField(default=0, null=False)
    status = models.CharField(
        max_length=20,
        choices=ProductStatusEnum.choices,
        default=ProductStatusEnum.NORMAL,
    )
