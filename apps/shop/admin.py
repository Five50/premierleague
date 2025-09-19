from django.contrib import admin
from .models import Category, Product, ProductVariation


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 0
    fields = ['size', 'color', 'quality', 'price', 'stock_quantity', 'in_stock']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'product_type', 'price', 'in_stock', 'created_at']
    list_filter = ['category', 'product_type', 'in_stock', 'created_at']
    search_fields = ['name', 'sku']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductVariationInline]

    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description', 'category', 'product_type')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'sku', 'in_stock', 'stock_quantity')
        }),
        ('Images', {
            'fields': ('featured_image', 'gallery_images')
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ['product', 'size', 'color', 'quality', 'price', 'stock_quantity', 'in_stock']
    list_filter = ['product__category', 'size', 'color', 'quality', 'in_stock']
    search_fields = ['product__name', 'sku']
