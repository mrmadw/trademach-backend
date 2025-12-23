# models.py
from django.db import models
from django.conf import settings

class Listing(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="listings"
    )

    title = models.CharField(max_length=255)
    description = models.TextField()

    price = models.DecimalField(max_digits=12, decimal_places=2)

    category = models.CharField(max_length=150)
    brand = models.CharField(max_length=150)

    condition = models.CharField(max_length=50)

    province = models.CharField(max_length=150)
    town = models.CharField(max_length=150)
    village = models.CharField(max_length=150, blank=True)

    address = models.CharField(max_length=255, blank=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
