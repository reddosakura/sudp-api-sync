# from services.users.repository.user_repository import UserRepository
# from services.users.users_service.exceptions import UserNotFoundException
from users.repository.user_repository import UserRepository
from .exceptions import UserNotFoundException


class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_user(self, user_id):
        return self.user_repository.get(user_id)

    def get_users_list(self, _show_deleted=False):
        return self.user_repository.list(_show_deleted)

    def get_user_by_login(self, login):
        return self.user_repository.get_by_login(login)

    def create_user(self, payload):
        return self.user_repository.add(payload)

    def delete_user(self, user_id):
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundException("Пользователь не найден. User not found")
        return self.user_repository.delete(user_id)

    def update_user(self, user_id, payload):
        user = self.user_repository.get(user_id)
        if user is None:
            raise UserNotFoundException("Пользователь не найден. User not found")
        return self.user_repository.update(user_id, payload)

    def create_roles(self):
        return self.user_repository.create_roles()

    def get_roles_list(self):
        return self.user_repository.get_roles()

    def get_role_by_name(self, name):
        return self.user_repository.get_role_by_name(name)
