from users.domain.entities.rol import Rol
from users.domain.entities.user import UserEntity


class CreateRoleUseCase:
    def __init__(self, role_repository):
        self.role_repository = role_repository

    def execute(self, role_name: str) -> Rol:
        clean_name = (role_name or '').strip().upper()
        if not clean_name:
            raise ValueError('El nombre del rol es obligatorio.')

        if self.role_repository.get_by_nombre(clean_name):
            raise ValueError(f"El rol '{clean_name}' ya existe.")

        rol = Rol(nombre=clean_name)
        return self.role_repository.create(rol)


class AssignRoleToUserUseCase:
    """Asigna `rol_id` al usuario (un solo rol en el modelo actual)."""

    def __init__(self, user_repository, role_repository):
        self.user_repository = user_repository
        self.role_repository = role_repository

    def execute(self, user_id: int, role_id: int):
        if not self.role_repository.get_by_id(role_id):
            raise LookupError('El rol que intentas asignar no existe.')

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise LookupError('Usuario no encontrado.')

        actualizado = UserEntity(
            id_user=user.id_user,
            nombre=user.nombre,
            apellido=user.apellido,
            email=user.email,
            activo=user.activo,
            rol_id=role_id,
            is_staff=user.is_staff,
            is_superuser=user.is_superuser,
            fecha_creacion=user.fecha_creacion,
        )
        result = self.user_repository.update(user_id, actualizado)
        if not result:
            raise LookupError('Usuario no encontrado.')
        return result
