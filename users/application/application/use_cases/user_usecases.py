from typing import Any, Dict, List, Optional

from users.domain.entities.user import UserEntity


class CreateUserUseCase:
    """Registra un usuario con contraseña en texto plano (el repositorio la hashea)."""

    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_data: Dict[str, Any]) -> UserEntity:
        email = (user_data.get('email') or '').strip().lower()
        nombre = (user_data.get('nombre') or '').strip()
        apellido = (user_data.get('apellido') or '').strip()
        password = (user_data.get('password') or '').strip()

        if not nombre or not apellido or not email:
            raise ValueError('Nombre, apellido y email son obligatorios.')
        if not password:
            raise ValueError('La contraseña es obligatoria.')
        if len(password) < 8:
            raise ValueError('La contraseña debe tener al menos 8 caracteres.')

        if self.user_repository.get_by_email(email):
            raise ValueError('El correo electrónico ya está registrado.')

        rol_id = user_data.get('rol_id')
        if rol_id is not None:
            try:
                rol_id = int(rol_id)
            except (TypeError, ValueError):
                rol_id = None

        entity = UserEntity(
            nombre=nombre,
            apellido=apellido,
            email=email,
            password=password,
            activo=bool(user_data.get('activo', True)),
            rol_id=rol_id,
            is_staff=bool(user_data.get('is_staff', False)),
            is_superuser=bool(user_data.get('is_superuser', False)),
        )
        return self.user_repository.create(entity)


class GetUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> UserEntity:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise LookupError('Usuario no encontrado.')
        return user


class GetUserByEmailUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, email: str) -> Optional[UserEntity]:
        return self.user_repository.get_by_email((email or '').strip().lower())


class ListUsersUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self) -> List[UserEntity]:
        return self.user_repository.get_all()


class UpdateUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int, user_data: Dict[str, Any]) -> UserEntity:
        actual = self.user_repository.get_by_id(user_id)
        if not actual:
            raise LookupError('Usuario no encontrado.')

        email = (user_data.get('email') or actual.email).strip().lower()
        nombre = (user_data.get('nombre') or actual.nombre).strip()
        apellido = (user_data.get('apellido') or actual.apellido).strip()

        if not nombre or not apellido or not email:
            raise ValueError('Nombre, apellido y email son obligatorios.')

        otro = self.user_repository.get_by_email(email)
        if otro and otro.id_user != user_id:
            raise ValueError('Ya existe otro usuario con ese email.')

        rol_raw = user_data.get('rol_id')
        if rol_raw is None and 'rol' in user_data:
            rol_raw = user_data.get('rol')
        if rol_raw in ('', None):
            rol_id = None
        else:
            try:
                rol_id = int(rol_raw)
            except (TypeError, ValueError):
                rol_id = actual.rol_id

        if 'activo' in user_data:
            activo = bool(user_data.get('activo'))
        else:
            activo = actual.activo
        if 'is_staff' in user_data:
            is_staff = bool(user_data.get('is_staff'))
        else:
            is_staff = actual.is_staff
        if 'is_superuser' in user_data:
            is_superuser = bool(user_data.get('is_superuser'))
        else:
            is_superuser = actual.is_superuser

        new_password = (user_data.get('new_password') or user_data.get('password') or '').strip() or None
        if new_password and len(new_password) < 8:
            raise ValueError('La nueva contraseña debe tener al menos 8 caracteres.')

        actualizado = UserEntity(
            id_user=actual.id_user,
            nombre=nombre,
            apellido=apellido,
            email=email,
            activo=activo,
            rol_id=rol_id,
            is_staff=is_staff,
            is_superuser=is_superuser,
            fecha_creacion=actual.fecha_creacion,
        )

        result = self.user_repository.update(user_id, actualizado, new_password=new_password)
        if not result:
            raise LookupError('Usuario no encontrado.')
        return result


class DeleteUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int) -> bool:
        if not self.user_repository.delete(user_id):
            raise LookupError('No se pudo eliminar el usuario (no existe).')
        return True
