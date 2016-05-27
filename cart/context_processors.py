from .cart import Cart

# держать корзину в контексте всех templates
def cart(request):
    return {'cart': Cart(request) }
