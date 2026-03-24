from users.domain.entities.mesa import Mesa
from users.infrastructure.models.mesa_model import MesaModel


class MesaRepositoryImpl:

    def _to_entity(self, model: MesaModel) -> Mesa:
        return Mesa(
            id_mesa=model.id_mesa,
            numero_mesa=model.numero_mesa,
            capacidad=model.capacidad,
            estado=model.estado,
            ubicacion=model.ubicacion,
            fecha_creacion=model.fecha_creacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in MesaModel.objects.all()]

    def get_by_id(self, mesa_id: int):
        try:
            return self._to_entity(MesaModel.objects.get(pk=mesa_id))
        except MesaModel.DoesNotExist:
            return None

    def get_by_estado(self, estado: str):
        return [self._to_entity(m) for m in MesaModel.objects.filter(estado=estado)]

    def create(self, mesa: Mesa) -> Mesa:
        model = MesaModel.objects.create(
            numero_mesa=mesa.numero_mesa,
            capacidad=mesa.capacidad,
            estado=mesa.estado,
            ubicacion=mesa.ubicacion,
        )
        return self._to_entity(model)

    def update(self, mesa_id: int, mesa: Mesa) -> Mesa:
        MesaModel.objects.filter(pk=mesa_id).update(
            numero_mesa=mesa.numero_mesa,
            capacidad=mesa.capacidad,
            estado=mesa.estado,
            ubicacion=mesa.ubicacion,
        )
        return self.get_by_id(mesa_id)

    def delete(self, mesa_id: int) -> bool:
        deleted, _ = MesaModel.objects.filter(pk=mesa_id).delete()
        return deleted > 0
