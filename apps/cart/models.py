from django.db import models
from django.contrib.sessions.models import Session
from decimal import Decimal
import json


class Cart(models.Model):
    session_key = models.CharField(max_length=40, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart {self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(models.Model):
    PRODUCT_TYPES = [
        ('variable', 'Variable Product'),
        ('single', 'Single Product'),
        ('multi-variable', 'Multi-Variable Product'),
    ]

    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES)
    product_id = models.CharField(max_length=100)  # e.g., 'malmo-ff-home-kit'
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # Product variations (JSON field for flexibility)
    variations = models.JSONField(default=dict, blank=True)  # e.g., {'size': 'M', 'color': 'blue'}

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('cart', 'product_type', 'product_id', 'variations')

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"

    def save(self, *args, **kwargs):
        # Ensure variations is always a dictionary
        if not isinstance(self.variations, dict):
            self.variations = {}
        super().save(*args, **kwargs)

    @property
    def total_price(self):
        return self.price * self.quantity

    @property
    def variations_display(self):
        """Return human-readable variations string"""
        if not self.variations:
            return ""

        # Handle case where variations might not be a dict (defensive programming)
        if not isinstance(self.variations, dict):
            return ""

        display_parts = []
        for key, value in self.variations.items():
            if key == 'size':
                display_parts.append(f"Size: {value}")
            elif key == 'color':
                display_parts.append(f"Color: {value}")
            elif key == 'quality':
                display_parts.append(f"Quality: {value}")
            else:
                display_parts.append(f"{key.title()}: {value}")

        return ", ".join(display_parts)
