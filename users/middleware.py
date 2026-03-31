"""Evita que el navegador guarde en caché páginas del panel; así, al cerrar sesión y usar «Atrás», se vuelve a validar con el servidor."""


class NoCacheAuthenticatedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            # Evita que proxies/CDN sirvan la misma página a otro usuario
            response['Vary'] = 'Cookie'
        return response
