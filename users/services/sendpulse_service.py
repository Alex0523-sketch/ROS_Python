import base64
import logging
import time
import uuid

import requests
from django.conf import settings

logger = logging.getLogger(__name__)

_SP_TOKEN_URL = 'https://api.sendpulse.com/oauth/access_token'
_SP_BASE = 'https://api.sendpulse.com'


def _get_token() -> str:
    resp = requests.post(
        _SP_TOKEN_URL,
        json={
            'grant_type': 'client_credentials',
            'client_id': settings.SENDPULSE_CLIENT_ID,
            'client_secret': settings.SENDPULSE_CLIENT_SECRET,
        },
        timeout=10,
    )
    if not resp.ok:
        raise RuntimeError(f'SendPulse auth error {resp.status_code}: {resp.text}')
    return resp.json()['access_token']


def _headers(token: str) -> dict:
    return {'Authorization': f'Bearer {token}'}


def _crear_lista_temporal(token: str, email: str, nombre: str) -> int:
    """Crea una lista de un solo contacto y retorna su book_id."""
    nombre_lista = f'reserva-tmp-{uuid.uuid4().hex[:8]}'
    resp = requests.post(
        f'{_SP_BASE}/addressbooks',
        json={'bookName': nombre_lista},
        headers=_headers(token),
        timeout=10,
    )
    if not resp.ok:
        raise RuntimeError(f'Error creando lista temporal: {resp.status_code} {resp.text}')
    book_id = resp.json()['id']

    resp = requests.post(
        f'{_SP_BASE}/addressbooks/{book_id}/emails',
        json={'emails': [{'email': email, 'variables': {'nombre': nombre}}]},
        headers=_headers(token),
        timeout=10,
    )
    if not resp.ok:
        raise RuntimeError(f'Error agregando contacto: {resp.status_code} {resp.text}')
    return book_id


def _eliminar_lista(token: str, book_id: int) -> None:
    """Elimina la lista temporal después de enviar."""
    requests.delete(
        f'{_SP_BASE}/addressbooks/{book_id}',
        headers=_headers(token),
        timeout=10,
    )


def _esperar_lista_lista(token: str, book_id: int, intentos: int = 6, espera: float = 3) -> None:
    """Espera hasta que la lista tenga al menos 1 contacto activo."""
    for _ in range(intentos):
        resp = requests.get(
            f'{_SP_BASE}/addressbooks/{book_id}',
            headers=_headers(token),
            timeout=10,
        )
        if resp.ok:
            data = resp.json()
            # La API devuelve lista o dict según versión
            info = data[0] if isinstance(data, list) else data
            if int(info.get('all_email_qty', 0)) > 0:
                return
        time.sleep(espera)
    raise RuntimeError('El contacto no se registró en SendPulse a tiempo.')


def _enviar_campana(token: str, book_id: int, subject: str, html: str) -> dict:
    """Lanza una campaña hacia el book_id dado."""
    campaign = {
        'sender_name': settings.SENDPULSE_FROM_NAME,
        'sender_email': settings.SENDPULSE_FROM_EMAIL,
        'subject': subject,
        'body': base64.b64encode(html.encode('utf-8')).decode('ascii'),
        'list_id': book_id,
    }
    for _ in range(5):
        resp = requests.post(
            f'{_SP_BASE}/campaigns',
            json=campaign,
            headers=_headers(token),
            timeout=15,
        )
        if resp.ok:
            return resp.json()
        code = resp.json().get('error_code')
        if code in (709, 798):  # lista bloqueada o vacía: esperar
            time.sleep(3)
            continue
        raise RuntimeError(f'Error creando campaña: {resp.status_code} {resp.text}')
    raise RuntimeError('Lista bloqueada en SendPulse. Intenta de nuevo.')


def _send_email(to_email: str, to_name: str, subject: str, html: str) -> dict:
    """Envía un correo individual usando el sistema de campañas de SendPulse."""
    token = _get_token()
    book_id = _crear_lista_temporal(token, to_email, to_name)
    try:
        _esperar_lista_lista(token, book_id)
        return _enviar_campana(token, book_id, subject, html)
    finally:
        _eliminar_lista(token, book_id)


def _build_html(titulo: str, mensaje: str, color_acento: str) -> str:
    return (
        '<!DOCTYPE html><html><head><meta charset="UTF-8"></head>'
        '<body style="margin:0;padding:0;background:#f5f0e8">'
        '<table width="100%" cellpadding="0" cellspacing="0" style="padding:32px 0">'
        '<tr><td align="center">'
        '<table width="560" cellpadding="0" cellspacing="0" '
        'style="background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,.10)">'
        '<tr><td style="background:#1a1a1a;padding:24px 32px;text-align:center">'
        '<h1 style="margin:0;font-family:Georgia,serif;font-size:26px;color:#ffd700">&#127869;&#65039; Olla y Saz&#243;n</h1>'
        '</td></tr>'
        f'<tr><td style="background:{color_acento};height:4px"></td></tr>'
        '<tr><td style="padding:32px">'
        f'<h2 style="margin:0 0 16px;font-size:20px;color:#1a1a1a;font-family:Georgia,serif">{titulo}</h2>'
        f'<p style="margin:0;font-size:15px;color:#444;line-height:1.7">{mensaje}</p>'
        '</td></tr>'
        '<tr><td style="background:#1a1a1a;padding:16px 32px;text-align:center">'
        '<p style="margin:0;font-size:12px;color:rgba(255,255,255,.5)">'
        '&copy; Restaurante Olla y Saz&#243;n &nbsp;|&nbsp; Gracias por elegirnos</p>'
        '</td></tr>'
        '</table></td></tr></table></body></html>'
    )


def _get_destinatario(reserva) -> tuple | None:
    """Retorna (email, nombre). Soporta usuarios autenticados y clientes públicos."""
    if reserva.user_id:
        from users.infrastructure.models import UserModel
        try:
            user = UserModel.objects.get(pk=reserva.user_id)
            return user.email, f'{user.nombre} {user.apellido}'.strip()
        except UserModel.DoesNotExist:
            pass

    if reserva.email_cliente:
        return reserva.email_cliente, (reserva.nombre_cliente or 'Cliente')

    return None


def enviar_correo_confirmacion(reserva) -> bool:
    """Envía correo de confirmación cuando el admin acepta la reserva."""
    destinatario = _get_destinatario(reserva)
    if not destinatario:
        logger.warning('Reserva %s sin email: no se envió confirmación.', reserva.pk)
        return False

    email, nombre = destinatario
    fecha = reserva.fecha_reserva.strftime('%d/%m/%Y') if reserva.fecha_reserva else '—'
    hora = reserva.hora or '—'

    html = _build_html(
        titulo='&#10003; Reserva Confirmada',
        mensaje=(
            f'Hola <strong>{nombre}</strong>,<br><br>'
            f'Tu reserva para el <strong>{fecha}</strong> a las <strong>{hora}</strong> '
            f'ha sido confirmada.<br><br>'
            f'Código de reserva: <strong>{reserva.codigo_reserva}</strong><br><br>'
            '¡Te esperamos con mucho gusto!'
        ),
        color_acento='#28a745',
    )

    try:
        _send_email(email, nombre, '✅ Reserva confirmada — Olla y Sazón', html)
        logger.info('Confirmación enviada a %s (reserva %s).', email, reserva.pk)
        return True
    except RuntimeError as exc:
        logger.error('Error enviando confirmación reserva %s: %s', reserva.pk, exc)
        return False


def enviar_correo_rechazo(reserva) -> bool:
    """Envía correo de rechazo cuando el admin cancela la reserva."""
    destinatario = _get_destinatario(reserva)
    if not destinatario:
        logger.warning('Reserva %s sin email: no se envió rechazo.', reserva.pk)
        return False

    email, nombre = destinatario

    html = _build_html(
        titulo='&#10007; Reserva No Disponible',
        mensaje=(
            f'Hola <strong>{nombre}</strong>,<br><br>'
            'Lamentamos informarte que tu reserva no pudo ser confirmada por disponibilidad.<br><br>'
            f'Código de reserva: <strong>{reserva.codigo_reserva}</strong><br><br>'
            'Si deseas intentarlo en otra fecha u hora, no dudes en contactarnos. '
            '¡Esperamos verte pronto!'
        ),
        color_acento='#dc3545',
    )

    try:
        _send_email(email, nombre, '❌ Reserva no disponible — Olla y Sazón', html)
        logger.info('Rechazo enviado a %s (reserva %s).', email, reserva.pk)
        return True
    except RuntimeError as exc:
        logger.error('Error enviando rechazo reserva %s: %s', reserva.pk, exc)
        return False
