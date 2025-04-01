import datetime
import uuid
from typing import List, Optional

from pydantic import BaseModel


class RoleSchema(BaseModel):
    id: uuid.UUID
    name: str


class UserBaseSchema(BaseModel):
    lastname: str
    name: str
    patronymic: str
    role_id: uuid.UUID
    speciality: str
    logged_in: bool
    is_deleted: bool
    login: str

    # is_deleted: bool
    # created_date: datetime.datetime = datetime.datetime.now()


# class UserSchema(UserBaseSchema):
#
#
#     class Config:
#         from_attributes = True

class UserReadSchema(UserBaseSchema):
    login: str
    role: RoleSchema
    id: uuid.UUID

    class Config:
        from_attributes = True

class CreateUserSchema(UserBaseSchema):
    login: str
    hashed_password: bytes

    class Config:
        from_attributes = True


class GetAllUsersSchema(BaseModel):
    users: List[UserReadSchema]


class GetAllRolesSchema(BaseModel):
    roles: List[RoleSchema]


class AuthSchema(BaseModel):
    login: str
    password: str

class AuthResponseSchema(BaseModel):
    authenticated: bool
    role: Optional[str]
    lnp: Optional[str]
    id: uuid.UUID