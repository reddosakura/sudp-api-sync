import sqlalchemy
from fastapi import APIRouter, HTTPException
from sqlalchemy.sql import roles
from starlette import status

from users.repository.database_unit import DatabaseUnit
from users.repository.user_repository import UserRepository
from werkzeug.security import generate_password_hash

from users.users_service.exceptions import UserNotFoundException, RolesDoesntExistException
from .schemas import GetAllUsersSchema, CreateUserSchema, UserBaseSchema, GetAllRolesSchema, RoleSchema, \
    UserReadSchema, AuthResponseSchema, AuthSchema
from users.users_service.users_service import UsersService

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.on_event("startup")
def startup():
    with DatabaseUnit() as unit:
        unit.initialize_tables()

    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            try:
                user_service.get_roles_list()
                print("ROLES ARE ALREADY INITIALIZED")
            except RolesDoesntExistException:
                user_service.create_roles()
                unit.commit()
                print("ROLES ARE INITIALIZED")

    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            try:
                user_service.get_user_by_login(login="admin")
            except UserNotFoundException:
                role = user_service.get_role_by_name("Суперпользователь")
                user = user_service.create_user(
                    CreateUserSchema(
                        lastname="Латышев",
                        name="Александр",
                        patronymic="Евгеньевич",
                        speciality="Специалист ОКиИТ",
                        role_id=role.id,
                        logged_in=False,
                        is_deleted=False,
                        login="admin",
                        hashed_password=generate_password_hash("1234qwerty",
                                                                 method="pbkdf2:sha256", salt_length=8),
                    )
                )
                print(user, "user_created")
                unit.commit()
                # user_service = UsersService(unit.session)

@router.get("/users", response_model=GetAllUsersSchema, tags=["Получение списка пользователей"])
def get_users(show_deleted: bool = False):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            print(show_deleted)
            results = user_service.get_users_list(_show_deleted=show_deleted)

    return {
        "users": [result.to_dict() for result in results],
    }


@router.get("/users/{user_id}", response_model=UserReadSchema, tags=['Получение одного пользователя'])
def get_user(user_id: str):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            try:
                repo = UserRepository(unit.session)
                user_service = UsersService(repo)
                result = user_service.get_user(user_id)
            except UserNotFoundException:
                raise HTTPException(
                    status_code=404, detail=f"Пользователя не существует"
                )
    return result.to_dict()


@router.get("/users/list/roles", response_model=GetAllRolesSchema, tags=['Получение списка ролей'])
def get_all_roles():
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            results = user_service.get_roles_list()
    return {
        "roles": [role.to_dict() for role in results]
    }


@router.post("/users/create", response_model=CreateUserSchema, tags=['Создание пользователя'])
def create_user(user: CreateUserSchema):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            try:
                repo = UserRepository(unit.session)
                user_service = UsersService(repo)
                creation = user_service.create_user(user)
                unit.commit()
            except sqlalchemy.exc.IntegrityError:
                raise HTTPException(
                    status_code=500, detail=f"Пользователь с таким логином уже существует"
                )
    created_user = creation.to_dict()
    created_user.update({"hashed_password": str.encode("0")})
    return created_user


@router.put("/users/update/base/{user_id}", response_model=UserBaseSchema, tags=['Редактирование основной информации о пользователе'])
def update_user(user_id: str, payload: UserBaseSchema):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            updated_user = user_service.update_user(user_id, payload)
            unit.commit()
    return updated_user.to_dict()


@router.put("/users/update/full/{user_id}", response_model=CreateUserSchema, tags=['Редактирование всей информации о пользователе'])
def update_user(user_id: str, payload: CreateUserSchema):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            updated_user = user_service.update_user(user_id, payload)
            unit.commit()
    _user = updated_user.to_dict()
    _user.update({"hashed_password": str.encode("0")})
    return _user


@router.delete("/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=['Логическое удаление пользователя'])
def delete_user(user_id: str):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = UserRepository(unit.session)
            user_service = UsersService(repo)
            user_service.delete_user(user_id)
            unit.commit()


@router.post("/auth", response_model=AuthResponseSchema, tags=["Авторизация"])
def auth_user(auth: AuthSchema):
    try:
        with DatabaseUnit() as unit:
            with unit.session.begin():
                repo = UserRepository(unit.session)
                user_service = UsersService(repo)
                user = user_service.get_user_by_login(auth.login)
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return user.authenticate(auth.password)
