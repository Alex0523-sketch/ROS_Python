#

class CreateRoleUseCase:
    def __init__(self, role_repository):
        self.role_repository = role_repository

    def execute(self, role_name: str):

        existing_role = self.role_repository.find_by_name(role_name)
        if existing_role:
            raise ValueError(f"El rol '{role_name}' ya existe.")

        clean_name = role_name.upper().strip()


        return self.role_repository.save({"name": clean_name})

class AssignRoleToUserUseCase:
    def __init__(self, user_repository, role_repository):

        self.user_repository = user_repository
        self.role_repository = role_repository

    def execute(self, user_id: int, role_id: int):

        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise Exception("Usuario no encontrado")

        role = self.role_repository.get_by_id(role_id)
        if not role:
            raise Exception("El rol que intentas asignar no existe")


        user.assign_role(role) 
        return self.user_repository.update(user)
