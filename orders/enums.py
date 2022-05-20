from django.db import models


class OrderStatusEnum(models.TextChoices):
    PROCESSING = "processing"
    CANCELED = "canceled"
    DELIVERED = "delivered"
