from django import template

from users.utils.money import format_money_display

register = template.Library()


@register.filter(name="money")
def money_filter(value, decimal_places=2):
    """
    Separa miles (.) y decimales (,). Por defecto 2 decimales.
    Uso: {{ precio|money }} o {{ entero|money:0 }}
    """
    if decimal_places is not None and decimal_places != "":
        try:
            dp = int(decimal_places)
        except (TypeError, ValueError):
            dp = 2
    else:
        dp = 2
    return format_money_display(value, decimal_places=dp)
