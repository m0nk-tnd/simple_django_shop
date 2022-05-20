from django.db import models


class ProductStatusEnum(models.TextChoices):
    NORMAL = "normal"
    ARCHIVED = "archived"
