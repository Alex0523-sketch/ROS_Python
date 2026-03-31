from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.cache import never_cache

from users.application.use_cases.user_usecases import CreateUserUseCase
from users.infrastructure.models import RolModel, UserModel
from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from users.infrastructure.views.auth_utils import post_login_redirect_url


class PasswordResetEmailView(auth_views.PasswordResetView):
    """Incluye `absolute_base` en el correo para que el enlace use el mismo host y puerto de la solicitud."""

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': {
                **(self.extra_email_context or {}),
                'absolute_base': self.request.build_absolute_uri('/').rstrip('/'),
            },
        }
        form.save(**opts)
        return HttpResponseRedirect(self.get_success_url())


def _safe_next_url(request):
    nxt = request.GET.get('next') or request.POST.get('next') or ''
    if not nxt:
        return None
    if url_has_allowed_host_and_scheme(
        nxt,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return nxt
    return None


def login_view(request):
    if request.user.is_authenticated:
        return redirect(post_login_redirect_url(request.user))

    if request.method == 'POST':
        email = (request.POST.get('username') or '').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user:
            if not user.is_active:
                messages.error(request, 'Tu cuenta está desactivada.')
                return render(
                    request,
                    'auth/login.html',
                    {'form_errors': True, 'next': request.POST.get('next', '')},
                )
            login(request, user)
            next_url = _safe_next_url(request)
            if next_url:
                return redirect(next_url)
            return redirect(post_login_redirect_url(user))
        return render(
            request,
            'auth/login.html',
            {'form_errors': True, 'next': request.POST.get('next', '')},
        )

    return render(request, 'auth/login.html', {'next': request.GET.get('next', '')})


@never_cache
def register_view(request):
    if request.user.is_authenticated:
        return redirect(post_login_redirect_url(request.user))

    rol_cliente = RolModel.objects.filter(nombre__iexact='CLIENTE').first()
    if not rol_cliente:
        messages.error(
            request,
            'No está configurado el rol CLIENTE en el sistema. Contacta al administrador.',
        )
        return redirect('login')

    if request.method == 'POST':
        nombre = (request.POST.get('nombre') or '').strip()
        apellido = (request.POST.get('apellido') or '').strip()
        email = (request.POST.get('email') or '').strip()
        password = (request.POST.get('password') or '').strip()
        password2 = (request.POST.get('password2') or '').strip()

        posted = {
            'nombre': nombre,
            'apellido': apellido,
            'email': email,
        }

        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'auth/register.html', {'posted': posted}, status=400)

        try:
            CreateUserUseCase(UserRepositoryImpl()).execute(
                {
                    'nombre': nombre,
                    'apellido': apellido,
                    'email': email,
                    'password': password,
                    'rol_id': rol_cliente.id_rol,
                    'activo': True,
                    'is_staff': False,
                    'is_superuser': False,
                }
            )
        except ValueError as exc:
            messages.error(request, str(exc))
            return render(request, 'auth/register.html', {'posted': posted}, status=400)

        user = UserModel.objects.get(email__iexact=email.lower())
        login(request, user)
        messages.success(request, '¡Cuenta creada! Ya puedes usar el sistema.')
        return redirect(post_login_redirect_url(user))

    return render(request, 'auth/register.html', {'posted': None})


@never_cache
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    response = redirect('login')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    # Ayuda a que el navegador no siga mostrando HTML del panel desde caché (Chrome/Edge/Firefox recientes)
    response['Clear-Site-Data'] = '"cache"'
    return response
