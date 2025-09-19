from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Product(models.Model):
    PRODUCT_TYPES = [
        ('single', 'Single Product'),
        ('variable', 'Variable Product'),
        ('multi-variable', 'Multi-Variable Product'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='single')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    # Basic pricing (for single products)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # Product details
    sku = models.CharField(max_length=50, unique=True, blank=True)
    in_stock = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=0)

    # SEO and metadata
    meta_description = models.CharField(max_length=160, blank=True)

    # Images
    featured_image = models.URLField(blank=True, help_text="URL to product image")
    gallery_images = models.JSONField(default=list, blank=True, help_text="List of image URLs")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        if not self.sku:
            self.sku = f"PROD-{self.slug.upper()}"
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product-detail', kwargs={'slug': self.slug})

    @property
    def get_price_range(self):
        """Get price range for variable products"""
        if self.product_type == 'single':
            return self.price

        variations = self.variations.all()
        if not variations:
            return self.price or 0

        prices = [v.price for v in variations if v.price]
        if not prices:
            return self.price or 0

        min_price = min(prices)
        max_price = max(prices)

        if min_price == max_price:
            return min_price
        return f"{min_price} - {max_price}"


class ProductVariation(models.Model):
    """Product variations for variable and multi-variable products"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')

    # Variation attributes
    size = models.CharField(max_length=20, blank=True)
    color = models.CharField(max_length=50, blank=True)
    quality = models.CharField(max_length=50, blank=True)  # For different qualities (Home, Away, Third, etc.)

    # Pricing and stock for this variation
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sku = models.CharField(max_length=50, unique=True, blank=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    in_stock = models.BooleanField(default=True)

    # Images specific to this variation
    featured_image = models.URLField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('product', 'size', 'color', 'quality')

    def __str__(self):
        parts = [self.product.name]
        if self.quality:
            parts.append(self.quality)
        if self.size:
            parts.append(f"Size {self.size}")
        if self.color:
            parts.append(self.color)
        return " - ".join(parts)

    def save(self, *args, **kwargs):
        if not self.sku:
            base_sku = self.product.sku or slugify(self.product.name).upper()
            variation_parts = []
            if self.size:
                variation_parts.append(self.size)
            if self.color:
                variation_parts.append(self.color[:3].upper())
            if self.quality:
                variation_parts.append(self.quality[:3].upper())

            if variation_parts:
                self.sku = f"{base_sku}-{'-'.join(variation_parts)}"
            else:
                self.sku = f"{base_sku}-VAR"

        super().save(*args, **kwargs)

    @property
    def variation_attributes(self):
        """Return dict of variation attributes for cart storage"""
        attrs = {}
        if self.size:
            attrs['size'] = self.size
        if self.color:
            attrs['color'] = self.color
        if self.quality:
            attrs['quality'] = self.quality
        return attrs
