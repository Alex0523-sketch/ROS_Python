from users.domain.entities.rol import Rol
from users.infrastructure.models.rol_model import RolModel


class RolRepositoryImpl:

    def _to_entity(self, model: RolModel) -> Rol:
        return Rol(
            id_rol=model.id_rol,
            nombre=model.nombre,
        )

    def get_all(self):
        return [self._to_entity(m) for m in RolModel.objects.all()]

    def get_by_id(self, rol_id: int):
        try:
            return self._to_entity(RolModel.objects.get(pk=rol_id))
        except RolModel.DoesNotExist:
            return None

    def get_by_nombre(self, nombre: str):
        try:
            return self._to_entity(RolModel.objects.get(nombre=nombre))
        except RolModel.DoesNotExist:
            return None

    def create(self, rol: Rol) -> Rol:
        model = RolModel.objects.create(nombre=rol.nombre)
        return self._to_entity(model)

    def update(self, rol_id: int, rol: Rol) -> Rol:
        RolModel.objects.filter(pk=rol_id).update(nombre=rol.nombre)
        return self.get_by_id(rol_id)

    def delete(self, rol_id: int) -> bool:
        deleted, _ = RolModel.objects.filter(pk=rol_id).delete()
        return deleted > 0
