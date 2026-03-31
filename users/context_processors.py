"""Variables globales de plantilla (carrito en sesión)."""

SESSION_CARRITO_KEY = 'public_carrito'


def carrito_publico(request):
    items = request.session.get(SESSION_CARRITO_KEY, [])
    count = sum(int(i.get('cantidad', 0)) for i in items)
    return {'carrito_count': count, 'carrito_items': items}
