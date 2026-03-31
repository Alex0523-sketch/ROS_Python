"""Formato de cantidades monetarias con separadores de miles (p. ej. 12.345,67)."""

from django.utils.numberformat import format as format_number


def format_money_display(value, decimal_places=2):
    """
    Formatea un número con agrupación cada 3 dígitos.
    Estilo es-CO / es: miles con punto, decimales con coma.
    """
    if value is None or value == "":
        return ""
    try:
        dp = int(decimal_places)
    except (TypeError, ValueError):
        dp = 2
    try:
        return format_number(
            value,
            ",",
            dp,
            3,
            ".",
            force_grouping=True,
            use_l10n=False,
        )
    except (TypeError, ValueError):
        return str(value)
