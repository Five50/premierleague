from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.urls import reverse
from decimal import Decimal
import json

from .models import Cart, CartItem


def get_or_create_cart(request):
    """Get or create a cart for the current session"""
    if not request.session.session_key:
        request.session.create()

    cart, created = Cart.objects.get_or_create(
        session_key=request.session.session_key
    )
    return cart


@require_POST
def add_to_cart(request):
    """Add item to cart via AJAX"""
    print(f"Add to cart - Request method: {request.method}")
    print(f"Add to cart - Content type: {request.content_type}")
    print(f"Add to cart - Session key: {request.session.session_key}")
    print(f"Add to cart - Request body: {request.body}")

    try:
        data = json.loads(request.body)

        product_type = data.get('product_type')
        product_id = data.get('product_id')
        product_name = data.get('product_name')
        price = Decimal(str(data.get('price', 0)))
        quantity = int(data.get('quantity', 1))
        variations = data.get('variations', {})

        # Validate required fields
        if not all([product_type, product_id, product_name, price]):
            return JsonResponse({
                'success': False,
                'error': 'Missing required product information'
            })

        cart = get_or_create_cart(request)

        # Try to find existing item with same variations
        existing_item = None
        try:
            existing_item = CartItem.objects.get(
                cart=cart,
                product_type=product_type,
                product_id=product_id,
                variations=variations
            )
            # Update quantity
            existing_item.quantity += quantity
            existing_item.save()
            item = existing_item
        except CartItem.DoesNotExist:
            # Create new item
            item = CartItem.objects.create(
                cart=cart,
                product_type=product_type,
                product_id=product_id,
                product_name=product_name,
                price=price,
                quantity=quantity,
                variations=variations
            )

        return JsonResponse({
            'success': True,
            'message': f'{product_name} added to cart',
            'cart_total_items': cart.total_items,
            'cart_total_price': float(cart.total_price),
            'item_id': item.id
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@require_POST
def update_cart_item(request, item_id):
    """Update cart item quantity"""
    try:
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        quantity = int(request.POST.get('quantity', 1))

        if quantity <= 0:
            item.delete()
            messages.success(request, f'{item.product_name} removed from cart')
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, f'{item.product_name} quantity updated')

        return redirect('cart:view_cart')

    except Exception as e:
        messages.error(request, f'Error updating cart: {str(e)}')
        return redirect('cart:view_cart')


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    try:
        cart = get_or_create_cart(request)
        item = get_object_or_404(CartItem, id=item_id, cart=cart)

        product_name = item.product_name
        item.delete()

        messages.success(request, f'{product_name} removed from cart')

    except Exception as e:
        messages.error(request, f'Error removing item: {str(e)}')

    return redirect('cart:view_cart')


def view_cart(request):
    """Display cart contents"""
    cart = get_or_create_cart(request)
    items = cart.items.all().order_by('-created_at')

    # Debug info
    print(f"Cart view - Session key: {request.session.session_key}")
    print(f"Cart view - Cart ID: {cart.id}")
    print(f"Cart view - Items count: {items.count()}")
    print(f"Cart view - Total items: {cart.total_items}")

    context = {
        'cart': cart,
        'items': items,
        'total_price': cart.total_price,
        'total_items': cart.total_items,
    }

    return render(request, 'pages/cart.html', context)


def get_cart_summary(request):
    """Get cart summary for AJAX requests"""
    cart = get_or_create_cart(request)

    return JsonResponse({
        'total_items': cart.total_items,
        'total_price': float(cart.total_price),
        'items': [
            {
                'id': item.id,
                'product_name': item.product_name,
                'quantity': item.quantity,
                'price': float(item.price),
                'total_price': float(item.total_price),
                'variations_display': item.variations_display,
            }
            for item in cart.items.all()
        ]
    })


def checkout(request):
    """Display checkout page"""
    cart = get_or_create_cart(request)
    items = cart.items.all()

    if not items:
        messages.warning(request, 'Your cart is empty. Add some items before checkout.')
        return redirect('cart:view_cart')

    # Calculate totals
    subtotal = cart.total_price
    free_delivery_threshold = 1000
    delivery_fee = 0 if subtotal >= free_delivery_threshold else 99
    total = subtotal + delivery_fee

    # Calculate amount needed for free delivery
    amount_for_free_delivery = max(0, free_delivery_threshold - subtotal)

    context = {
        'cart': cart,
        'items': items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total_price': total,
        'free_delivery_threshold': free_delivery_threshold,
        'amount_for_free_delivery': amount_for_free_delivery,
    }

    return render(request, 'pages/checkout.html', context)


def cart_api_data(request):
    """API endpoint to get cart data for Alpine.js"""
    cart = get_or_create_cart(request)
    items = cart.items.all()

    # Convert cart items to API format
    items_data = []
    for item in items:
        items_data.append({
            'id': item.id,
            'cartItemId': item.id,  # For Alpine.js compatibility
            'product_name': item.product_name,
            'product_type': item.product_type,
            'product_id': item.product_id,
            'price': float(item.price),
            'quantity': item.quantity,
            'variations': item.variations if isinstance(item.variations, dict) else {},
            'total_price': float(item.total_price),
        })

    # Calculate totals
    subtotal = float(cart.total_price)
    free_delivery_threshold = 1000
    shipping = 0 if subtotal >= free_delivery_threshold else 99
    total = subtotal + shipping

    return JsonResponse({
        'success': True,
        'items': items_data,
        'subtotal': subtotal,
        'shipping': shipping,
        'total': total,
        'item_count': cart.total_items,
    })
