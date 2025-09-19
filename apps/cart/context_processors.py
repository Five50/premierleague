"""
Cart context processors.
"""

from .models import Cart


def cart_data(request):
    """Add cart data to all templates."""
    cart = None
    cart_items_count = 0

    if request.session.session_key:
        try:
            cart = Cart.objects.get(session_key=request.session.session_key)
            cart_items_count = cart.total_items
        except Cart.DoesNotExist:
            pass

    return {
        'cart_items_count': cart_items_count,
        'current_cart': cart,
    }