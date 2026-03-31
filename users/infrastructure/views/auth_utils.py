from django.conf import settings
from django.shortcuts import resolve_url
from django.urls import NoReverseMatch


def post_login_redirect_url(user):
    """Destino tras login según rol (nombres en BD: ADMINISTRADOR, CLIENTE, EMPLEADO)."""
    r = getattr(user, 'rol', None)
    nombre = (r.nombre or '').strip().upper() if r else ''
    if nombre in ('ADMIN', 'ADMINISTRADOR'):
        nombre = 'ADMINISTRADOR'

    if nombre == 'ADMINISTRADOR':
        try:
            return resolve_url('admin_dashboard')
        except NoReverseMatch:
            return '/dashboard/'
    if user.is_superuser:
        try:
            return resolve_url('admin:index')
        except NoReverseMatch:
            return '/admin/'
    if nombre == 'CLIENTE':
        try:
            return resolve_url('mi_perfil')
        except NoReverseMatch:
            return '/mi-perfil/'
    if nombre == 'EMPLEADO':
        try:
            return resolve_url('mi_horario')
        except NoReverseMatch:
            return '/mi-horario/'

    return getattr(settings, 'LOGIN_REDIRECT_URL', '/') or '/'
