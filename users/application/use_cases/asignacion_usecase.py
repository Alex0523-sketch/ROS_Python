from django.db.models import Count, Q

from users.infrastructure.models.pedido_model import PedidoModel
from users.infrastructure.models.user_model import User

# Estados que cuentan como "pedido en marcha" para el empleado
ESTADOS_EN_MARCHA = ('CONFIRMADO', 'PENDIENTE', 'EN_PREPARACION', 'LISTO')
MAX_PEDIDOS_POR_EMPLEADO = 2


class AsignarEmpleadoPedidoUseCase:
    """
    Busca el empleado activo con menor carga de pedidos en marcha
    y lo asigna al pedido. Si todos tienen el maximo, deja sin asignar.
    """

    def execute(self, pedido_id: int):
        empleado = self._empleado_disponible()
        if empleado:
            PedidoModel.objects.filter(pk=pedido_id).update(empleado_asignado=empleado)
        return empleado

    def _empleado_disponible(self):
        return (
            User.objects.filter(activo=True, rol__nombre__iexact='EMPLEADO')
            .annotate(
                pedidos_en_marcha=Count(
                    'pedidos_asignados',
                    filter=Q(pedidos_asignados__estado__in=ESTADOS_EN_MARCHA),
                )
            )
            .filter(pedidos_en_marcha__lt=MAX_PEDIDOS_POR_EMPLEADO)
            .order_by('pedidos_en_marcha', 'id_user')
            .first()
        )
