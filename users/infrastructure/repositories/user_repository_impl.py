from users.domain.entities.user import UserEntity
from users.infrastructure.models.user_model import User as UserModel


class UserRepositoryImpl:

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id_user=model.id_user,
            nombre=model.nombre,
            apellido=model.apellido,
            email=model.email,
            password=model.password,
            activo=model.activo,
            rol_id=model.rol_id,
            fecha_creacion=model.fecha_creacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in UserModel.objects.all()]

    def get_by_id(self, user_id: int):
        try:
            return self._to_entity(UserModel.objects.get(pk=user_id))
        except UserModel.DoesNotExist:
            return None

    def get_by_email(self, email: str):
        try:
            return self._to_entity(UserModel.objects.get(email=email))
        except UserModel.DoesNotExist:
            return None

    def create(self, user: UserEntity) -> UserEntity:
        model = UserModel.objects.create(
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email,
            password=user.password,
            activo=user.activo,
            rol_id=user.rol_id,
        )
        return self._to_entity(model)

    def update(self, user_id: int, user: UserEntity) -> UserEntity:
        UserModel.objects.filter(pk=user_id).update(
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email,
            activo=user.activo,
            rol_id=user.rol_id,
        )
        return self.get_by_id(user_id)

    def delete(self, user_id: int) -> bool:
        deleted, _ = UserModel.objects.filter(pk=user_id).delete()
        return deleted > 0
