from .models import Cart


def get_current_cart() -> Cart:
    """return users current cart"""
    cart, _ = Cart.objects.get_or_create(is_editable=True)
    return cart
