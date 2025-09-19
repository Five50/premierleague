from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from django.core.paginator import Paginator

from .models import Product, Category, ProductVariation


class ShopView(ListView):
    """Main shop view showing all products with filtering"""
    model = Product
    template_name = 'pages/shop.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(in_stock=True)

        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get('category')
        context['search_query'] = self.request.GET.get('search', '')
        return context


class ProductDetailView(DetailView):
    """Product detail view with variations"""
    model = Product
    template_name = 'pages/product-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Get product variations if any
        variations = product.variations.filter(in_stock=True)
        context['variations'] = variations

        # Group variations for display
        if variations:
            sizes = list(set(v.size for v in variations if v.size))
            colors = list(set(v.color for v in variations if v.color))
            qualities = list(set(v.quality for v in variations if v.quality))

            context['available_sizes'] = sorted(sizes) if sizes else []
            context['available_colors'] = colors
            context['available_qualities'] = qualities

        # Related products
        context['related_products'] = Product.objects.filter(
            category=product.category,
            in_stock=True
        ).exclude(id=product.id)[:4]

        return context


def get_product_variation(request):
    """AJAX endpoint to get variation details"""
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    product_id = request.GET.get('product_id')
    size = request.GET.get('size', '')
    color = request.GET.get('color', '')
    quality = request.GET.get('quality', '')

    try:
        product = Product.objects.get(id=product_id)

        # Try to find exact variation
        variation = None
        if product.product_type != 'single':
            try:
                variation = ProductVariation.objects.get(
                    product=product,
                    size=size,
                    color=color,
                    quality=quality,
                    in_stock=True
                )
            except ProductVariation.DoesNotExist:
                return JsonResponse({
                    'error': 'This variation is not available',
                    'available': False
                })

        # Return product/variation data
        if variation:
            return JsonResponse({
                'available': True,
                'price': float(variation.price),
                'stock_quantity': variation.stock_quantity,
                'sku': variation.sku,
                'image': variation.featured_image or product.featured_image,
                'variation_id': variation.id
            })
        else:
            # Single product
            return JsonResponse({
                'available': True,
                'price': float(product.price) if product.price else 0,
                'stock_quantity': product.stock_quantity,
                'sku': product.sku,
                'image': product.featured_image,
                'variation_id': None
            })

    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
