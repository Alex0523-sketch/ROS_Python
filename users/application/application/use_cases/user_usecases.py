
class CreateUserUseCase:
    def __init__(self, user_repository):

        self.user_repository = user_repository

    def execute(self, user_data: dict):

        existing_user = self.user_repository.get_by_email(user_data['email'])
        if existing_user:
            raise ValueError("El correo electrónico ya está registrado.")


        new_user = self.user_repository.save(user_data)


        return new_user

class GetUserUseCase:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def execute(self, user_id: int):
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise Exception("Usuario no encontrado")
        return user