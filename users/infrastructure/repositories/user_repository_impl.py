from users.domain.entities.user import UserEntity
from users.domain.repositories.user_repository import UserRepository
from users.infrastructure.models.user_model import User as UserModel


class UserRepositoryImpl(UserRepository):

    def _to_entity(self, model: UserModel) -> UserEntity:
        return UserEntity(
            id_user=model.id_user,
            nombre=model.nombre,
            apellido=model.apellido,
            email=model.email,
            password=None,
            activo=model.activo,
            rol_id=model.rol_id,
            is_staff=model.is_staff,
            is_superuser=model.is_superuser,
            fecha_creacion=model.fecha_creacion,
        )

    def get_all(self):
        return [self._to_entity(m) for m in UserModel.objects.all().order_by('nombre', 'apellido')]

    def get_by_id(self, user_id: int):
        try:
            return self._to_entity(UserModel.objects.get(pk=user_id))
        except UserModel.DoesNotExist:
            return None

    def get_by_email(self, email: str):
        try:
            return self._to_entity(UserModel.objects.get(email__iexact=email.strip()))
        except UserModel.DoesNotExist:
            return None

    def create(self, user: UserEntity) -> UserEntity:
        plain = (user.password or '').strip()
        if not plain:
            raise ValueError('La contraseña es obligatoria para crear un usuario.')
        model = UserModel(
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email.strip().lower(),
            activo=user.activo,
            rol_id=user.rol_id,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
        model.set_password(plain)
        model.save()
        return self._to_entity(model)

    def update(self, user_id: int, user: UserEntity, *, new_password: str | None = None) -> UserEntity | None:
        if not UserModel.objects.filter(pk=user_id).exists():
            return None
        UserModel.objects.filter(pk=user_id).update(
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email.strip().lower(),
            activo=user.activo,
            rol_id=user.rol_id,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
        )
        if new_password and new_password.strip():
            u = UserModel.objects.get(pk=user_id)
            u.set_password(new_password.strip())
            u.save(update_fields=['password'])
        return self.get_by_id(user_id)

    def delete(self, user_id: int) -> bool:
        deleted, _ = UserModel.objects.filter(pk=user_id).delete()
        return deleted > 0
