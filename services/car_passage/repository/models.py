
import uuid
from datetime import datetime, time
from typing import List, Annotated
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship, DeclarativeBase
)


class SqlAlchemyBase(DeclarativeBase):
    pass


current_date = Annotated[datetime, mapped_column(default=datetime.now)]
primary_key = Annotated[uuid.UUID, mapped_column(primary_key=True, default=uuid.uuid4)]

class HolidayDatesModel(SqlAlchemyBase):
    __tablename__ = 'holiday_dates'
    id: Mapped[primary_key]
    from_date: Mapped[datetime]
    to_date: Mapped[datetime]

    def to_dict(self):
        return {
            'id': self.id,
            'from_date': self.from_date,
            'to_date': self.to_date,
        }

    # BACK POPULATE


class FileModel(SqlAlchemyBase):
    __tablename__ = 'file'
    id: Mapped[primary_key]
    path: Mapped[str]
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'path': self.path,
            'request_id': self.request_id,
        }

    # BACK POPULATE
    # request: Mapped['RequestMainModel'] = relationship(back_populates="files")


class RequestTypeModel(SqlAlchemyBase):
    __tablename__ = 'request_type'
    id: Mapped[primary_key]
    name: Mapped[str]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    # BACK POPULATE
    # requests: Mapped[List['RequestMainModel']] = relationship(back_populates='request_type')


class RequestStatusModel(SqlAlchemyBase):
    __tablename__ = 'request_status'
    id: Mapped[primary_key]
    name: Mapped[str]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    # BACK POPULATE
    # requests: Mapped['RequestMainModel'] = relationship(back_populates="request_status")


class PassageModeModel(SqlAlchemyBase):
    __tablename__ = 'passmode'
    id: Mapped[primary_key]
    name: Mapped[str]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }
    # BACK POPULATE
    # requests: Mapped[List['RequestMainModel']] = relationship(back_populates="passmode")


class TransportTypeModel(SqlAlchemyBase):
    __tablename__ = 'transport_type'
    id: Mapped[primary_key]
    type: Mapped[str]

    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            # 'cars': [car.to_dict() for car in self.cars],
        }

    # BACK POPULATE
    cars: Mapped[List['CarModel']] = relationship(back_populates='transport_type', lazy='selectin')


class RequestMainModel(SqlAlchemyBase):
    __tablename__ = 'request_main'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('request_type.id'))
    contract_name: Mapped[str] = mapped_column(index=True)
    organization: Mapped[str] = mapped_column(index=True)
    from_date: Mapped[datetime]
    to_date: Mapped[datetime]
    from_time: Mapped[time]
    to_time: Mapped[time]
    comment: Mapped[str]
    # request_type_id: Mapped[int] = mapped_column(ForeignKey('request_type.id'))
    request_status_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('request_status.id'))
    passmode_id: Mapped[uuid.UUID] = mapped_column(ForeignKey('passmode.id'))
    creator: Mapped[int] = mapped_column(ForeignKey('user.id'))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    date_created: Mapped[current_date]

    # BACK POPULATE
    visitors: Mapped[List['VisitorModel']] = relationship(lazy='selectin')
    cars: Mapped[List['CarModel']] = relationship(lazy='selectin')
    creatorobj: Mapped['UserModel'] = relationship(lazy='selectin')
    request_type: Mapped['RequestTypeModel'] = relationship(lazy='selectin')
    passmode: Mapped['PassageModeModel'] = relationship(lazy='selectin')
    status: Mapped['RequestStatusModel'] = relationship(lazy='selectin')
    files: Mapped[List['FileModel']] = relationship(lazy='selectin')
    # request_type: Mapped['RequestTypeModel'] = relationship(back_populates="requests")
    # passmode: Mapped['PassageModeModel'] = relationship(back_populates="requests")
    # status: Mapped['RequestStatusModel'] = relationship(back_populates="requests")
    # files: Mapped[List['FileModel']] = relationship(back_populates="requests")
    # approval_comments: Mapped[List['ApprovalCommentsModel']] = relationship(back_populates='request')

    def to_dict(self):
        return {
            'id': self.id,
            'date_created': self.date_created,
            'type_id': self.type_id,
            'contract_name': self.contract_name,
            'organization': self.organization,
            'from_date': self.from_date,
            'to_date': self.to_date,
            'from_time': self.from_time,
            'to_time': self.to_time,
            'comment': self.comment,
            'request_status_id': self.request_status_id,
            'passmode_id': self.passmode_id,
            "creator": self.creator,
            "is_deleted": self.is_deleted,
            'passmode': self.passmode,
            'status': self.status,
            'files': [file.to_dict() for file in self.files],
            'request_type': self.request_type.to_dict(),
            'visitors': [visitor.to_dict() for visitor in self.visitors],
            'cars': [car.to_dict() for car in self.cars],
        }


class CarModel(SqlAlchemyBase):
    __tablename__ = 'car'
    id: Mapped[primary_key]
    govern_num: Mapped[str] = mapped_column(index=True)
    car_model: Mapped[str]
    passed_status: Mapped[bool]
    type_id: Mapped[int] = mapped_column(ForeignKey('transport_type.id'))
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'), nullable=True)
    visitor_id: Mapped[int] = mapped_column(ForeignKey('visitor.id'), nullable=True)
    is_deleted: Mapped[bool]
    date_deleted: Mapped[datetime] = mapped_column(nullable=True)
    date_created: Mapped[current_date]

    # BACK POPULATE
    driver: Mapped['VisitorModel'] = relationship(lazy='selectin')
    transport_type: Mapped['TransportTypeModel'] = relationship(back_populates='cars', lazy='selectin')
    # request: Mapped['RequestMainModel'] = relationship(back_populates='cars', lazy='selectin')
    # passages: Mapped[List['CarPassageModel']] = relationship(back_populates='car', lazy='selectin')

    def to_dict(self):
        return {
            'id': self.id,
            'govern_num': self.govern_num,
            'car_model': self.car_model,
            'passed_status': self.passed_status,
            'type_id': self.type_id,
            'request_id': self.request_id,
            "visitor_id": self.visitor_id,
            "is_deleted": self.is_deleted,
            'date_deleted': self.date_deleted,
            'date_created': self.date_created,
            'driver': self.driver.to_dict() if self.driver else None,
            'transport_type': self.transport_type.to_dict(),
            # 'passages': self.passages,
        }


class CarPassageModel(SqlAlchemyBase):
    __tablename__ = 'car_passage'
    id: Mapped[primary_key]
    pass_date: Mapped[current_date]
    status: Mapped[bool]
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'))

    # BACK POPULATE
    car: Mapped['CarModel'] = relationship(lazy='selectin')

    def to_dict(self):
        return {
            'id': self.id,
            'car_id': self.car_id,
            'status': self.status,
            'car': self.car.to_dict(),
        }


class RoleModel(SqlAlchemyBase):
    __tablename__ = 'role'
    id: Mapped[primary_key]
    name: Mapped[str]

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
        }

    # BACK POPULATE
    # users: Mapped[List['UserModel']] = relationship(back_populates='role')


class UserModel(SqlAlchemyBase):
    __tablename__ = 'user'
    id: Mapped[primary_key]
    lastname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str]
    role_id: Mapped['RoleModel'] = mapped_column(ForeignKey('role.id'))
    logged_in: Mapped[bool]
    login: Mapped[str] = mapped_column(unique=True)
    speciality: Mapped[str]
    hashed_password: Mapped[bytes]
    is_deleted: Mapped[bool]
    created_date: Mapped[current_date]

    # BACK POPULATE
    role: Mapped['RoleModel'] = relationship(lazy='selectin')
    # requests: Mapped[List['RequestMainModel']] = relationship(back_populates='creatorobj')
    # approval_comments: Mapped[List['ApprovalCommentsModel']] = relationship(back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'lastname': self.lastname,
            'name': self.name,
            'patronymic': self.patronymic,
            'role_id': self.role_id,
            'logged_in': self.logged_in,
            'login': self.login,
            'speciality': self.speciality,
            'hashed_password': self.hashed_password,
            'is_deleted': self.is_deleted,
            'created_date': self.created_date,
            'role': self.role.to_dict(),
        }


class VisitorModel(SqlAlchemyBase):
    __tablename__ = 'visitor'
    id: Mapped[primary_key]
    lastname: Mapped[str] = mapped_column(index=True)
    name: Mapped[str] = mapped_column(index=True)
    patronymic: Mapped[str] = mapped_column(index=True)
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'))
    passed_status: Mapped[bool]
    is_deleted: Mapped[bool]
    date_deleted: Mapped[datetime] = mapped_column(nullable=True)
    date_created: Mapped[current_date]

    # BACK POPULATE
    # request: Mapped['RequestMainModel'] = relationship(back_populates='visitors')
    car: Mapped['CarModel'] = relationship(back_populates='driver', lazy='selectin')
    passages: Mapped[List['VisitorPassageModel']] = relationship(lazy='selectin')

    def to_dict(self):
        return {
            'id': self.id,
            'lastname': self.lastname,
            'name': self.name,
            'patronymic': self.patronymic,
            'request_id': self.request_id,
            'passed_status': self.passed_status,
            'is_deleted': self.is_deleted,
            'date_deleted': self.date_deleted,
            'date_created': self.date_created,
            'passages': [passage.to_dict() for passage in self.passages],

        }


class VisitorPassageModel(SqlAlchemyBase):
    __tablename__ = 'visitor_passage'
    id: Mapped[primary_key]
    pass_date: Mapped[current_date]
    status: Mapped[bool]
    visitor_id: Mapped[int] = mapped_column(ForeignKey('visitor.id'))

    # BACK POPULATE
    visitor: Mapped['VisitorModel'] = relationship(back_populates='passages', lazy='selectin')

    def to_dict(self):
        return {
            'id': self.id,
            'pass_date': self.pass_date,
            'status': self.status,
            'visitor_id': self.visitor_id,
        }


class ApprovalCommentsModel(SqlAlchemyBase):
    __tablename__ = 'approval_comments'
    id: Mapped[primary_key]
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    request_status_id: Mapped[int] = mapped_column(ForeignKey('request_status.id'))
    comment: Mapped[str]
    created_date: Mapped[current_date]

    # BACK POPULATE
    status: Mapped['RequestStatusModel'] = relationship(lazy='selectin')
    # request: Mapped['RequestMainModel'] = relationship(back_populates='approval_comments')
    # user: Mapped['UserModel'] = relationship(lazy='selectin')

    def to_dict(self):
        return {
            'id': self.id,
            'request_id': self.request_id,
            'user_id': self.user_id,
            'request_status_id': self.request_status_id,
            'comment': self.comment,
            'status': self.status.to_dict(),
            'created_date': self.created_date
        }
