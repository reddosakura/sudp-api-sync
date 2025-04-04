import uuid

from sqlalchemy import select, insert, update

from users.users_service.exceptions import UserNotFoundException, RolesDoesntExistException
from .models import UserModel, RoleModel
from users.users_service.user import User, Role


class UserRepository:
    def __init__(self, session):
        self.session = session

    def add(self, user):
        payload = user.model_dump()
        print("user_created")
        self.session.execute(
            insert(UserModel).values(payload)
        )
        return User(**payload)

    def get(self, id_):
        user = (self.session.execute(select(UserModel).where(UserModel.id == str(id_)))).scalar()

        if user is None:
            raise UserNotFoundException("User not found. по данному ID пользвоатель не найден")

        return user

    def get_by_login(self, login):
        user = ((
            self.session.execute(
                select(UserModel).where(UserModel.login == login))
        )).scalar()
        print(user, "<-- user")

        if user is None:
            raise UserNotFoundException("User not found by login. Пользователь с данным логином не найден")

        return User(**user.to_dict())


    def list(self, _show_deleted: bool):
        query = select(UserModel).where(UserModel.is_deleted == False)
        if _show_deleted:
            query = select(UserModel)
        fetched_data = self.session.execute(query)
        return [User(**(data.to_dict())) for data in fetched_data.scalars()]

    def update(self, id_, payload):
        self.session.execute(update(UserModel)
                              .filter(UserModel.id == str(id_))
                              .values(payload.model_dump()))
        return User(**payload.model_dump())

    def delete(self, id_):
        self.session.execute(update(UserModel).where(UserModel.id == str(id_)).values(is_deleted=True))

    def create_roles(self):
        self.session.execute(
            insert(RoleModel),
            [
                {
                    "name": "Суперпользователь"
                },
                {
                    "name": "Администратор"
                },
                {
                    "name": "Ограниченное администрирование"
                },
                {
                    "name": "Заявитель"
                },
                {
                    "name": "Охрана"
                }
            ]
        )


    def get_roles(self):
        fetched_data = self.session.execute(
            select(RoleModel)
        )

        roles = list(fetched_data.scalars())
        print(list(roles), "<-- roles list")

        if not list(roles):
            print(list(roles), "<-- raised")
            raise RolesDoesntExistException("Roles doesnt exist in database. Роли не были инициализированы")

        return [Role(**data.to_dict()) for data in roles]


    def get_role_by_name(self, name):
        role = (self.session.execute(
            select(RoleModel).where(RoleModel.name == name)
        )).scalar()

        return Role(**(role.to_dict()))
