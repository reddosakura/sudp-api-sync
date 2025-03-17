import uuid
from datetime import datetime, time
from typing import List, Annotated
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from .handler import SqlAlchemyBase


current_date = Annotated[datetime, mapped_column(default=datetime.now)]
primary_key = Annotated[uuid.UUID, mapped_column(primary_key=True)]

class HolidayDates(SqlAlchemyBase):
    __tablename__ = 'holiday_dates'
    id: Mapped[primary_key]
    from_date: Mapped[datetime]
    to_date: Mapped[datetime]

    # BACK POPULATE


class File(SqlAlchemyBase):
    __tablename__ = 'file'
    id: Mapped[primary_key]
    path: Mapped[str]
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'))

    # BACK POPULATE
    # request: Mapped['RequestMain'] = relationship(back_populates="files")


class RequestType(SqlAlchemyBase):
    __tablename__ = 'request_type'
    id: Mapped[primary_key]
    name: Mapped[str]

    # BACK POPULATE
    # requests: Mapped[List['RequestMain']] = relationship(back_populates='request_type')


class RequestStatus(SqlAlchemyBase):
    __tablename__ = 'request_status'
    id: Mapped[primary_key]
    name: Mapped[str]

    # BACK POPULATE
    # requests: Mapped['RequestMain'] = relationship(back_populates="request_status")


class PassageMode(SqlAlchemyBase):
    __tablename__ = 'passmode'
    id: Mapped[primary_key]
    name: Mapped[str]

    # BACK POPULATE
    # requests: Mapped[List['RequestMain']] = relationship(back_populates="passmode")


class TransportType(SqlAlchemyBase):
    __tablename__ = 'transport_type'
    id: Mapped[primary_key]
    type: Mapped[str]

    # BACK POPULATE
    cars: Mapped[List['Car']] = relationship(back_populates='transport_type')


class RequestMain(SqlAlchemyBase):
    __tablename__ = 'request_main'
    id: Mapped[int] = mapped_column(primary_key=True)
    type_id: Mapped[int] = mapped_column(ForeignKey('request_type.id'))
    contract_name: Mapped[str] = mapped_column(index=True)
    organization: Mapped[str] = mapped_column(index=True)
    from_date: Mapped[datetime]
    to_date: Mapped[datetime]
    from_time: Mapped[time]
    to_time: Mapped[time]
    comment: Mapped[str]
    request_type_id: Mapped[int] = mapped_column(ForeignKey('request_type.id'))
    request_status_id: Mapped[int] = mapped_column(ForeignKey('request_status.id'))
    passmode_id: Mapped[int] = mapped_column(ForeignKey('passmode.id'))
    creator: Mapped[int] = mapped_column(ForeignKey('user.id'))
    is_deleted: Mapped[bool] = mapped_column(default=False)

    # BACK POPULATE
    visitors: Mapped[List['Visitor']] = relationship(back_populates='request')
    cars: Mapped[List['Car']] = relationship(back_populates='request')
    creatorobj: Mapped['UserModel'] = relationship(back_populates='requests')
    request_type: Mapped['RequestType'] = relationship(back_populates='requests')
    passmode: Mapped['PassageMode'] = relationship(back_populates='requests')
    status: Mapped['RequestStatus'] = relationship(back_populates='requests')
    files: Mapped[List['File']] = relationship(back_populates='request')
    approval_comments: Mapped[List['ApprovalComments']] = relationship(back_populates='request')


class Car(SqlAlchemyBase):
    __tablename__ = 'car'
    id: Mapped[primary_key]
    govern_num: Mapped[str] = mapped_column(index=True)
    passed_status: Mapped[bool]
    type_id: Mapped[int] = mapped_column(ForeignKey('transport_type.id'))
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'))
    visitor_id: Mapped[int] = mapped_column(ForeignKey('visitor.id'), nullable=True)
    date_deleted: Mapped[datetime] = mapped_column(nullable=True)
    date_created: Mapped[current_date]

    # BACK POPULATE
    driver: Mapped['Visitor'] = relationship(back_populates='car')
    transport_type: Mapped['TransportType'] = relationship(back_populates='cars')
    request: Mapped['TransportType'] = relationship(back_populates='cars')
    passages: Mapped[List['CarPassage']] = relationship(back_populates='car')
    # type: Mapped['RequestType'] = relationship(back_populates='request')


class CarPassage(SqlAlchemyBase):
    __tablename__ = 'car_passage'
    id: Mapped[primary_key]
    pass_date: Mapped[current_date]
    status: Mapped[bool]
    car_id: Mapped[int] = mapped_column(ForeignKey('car.id'))

    # BACK POPULATE
    car: Mapped['Car'] = relationship(back_populates='passages')


class Role(SqlAlchemyBase):
    __tablename__ = 'role'
    id: Mapped[primary_key]
    name: Mapped[str]

    # BACK POPULATE
    users: Mapped[List['UserModel']] = relationship(back_populates='role')


class UserModel(SqlAlchemyBase):
    __tablename__ = 'user'
    id: Mapped[primary_key]
    lastname: Mapped[str]
    name: Mapped[str]
    patronymic: Mapped[str]
    role_id: Mapped['Role'] = mapped_column(ForeignKey('role.id'))
    logged_id: Mapped[bool]
    login: Mapped[str]
    speciality: Mapped[str]
    hashed_password: Mapped[bytes]
    is_deleted: Mapped[bool]
    created_date: Mapped[current_date]

    # BACK POPULATE
    role: Mapped['Role'] = relationship(back_populates='users')
    requests: Mapped[List['RequestMain']] = relationship(back_populates='creatorobj')
    approval_comments: Mapped[List['ApprovalComments']] = relationship(back_populates='user')


class Visitor(SqlAlchemyBase):
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
    request: Mapped['RequestMain'] = relationship(back_populates='visitors')
    car: Mapped['Car'] = relationship(back_populates='driver')
    passages: Mapped[List['VisitorPassage']] = relationship(back_populates='visitor')


class VisitorPassage(SqlAlchemyBase):
    __tablename__ = 'visitor_passage'
    id: Mapped[primary_key]
    pass_date: Mapped[current_date]
    status: Mapped[bool]
    visitor_id: Mapped[int] = mapped_column(ForeignKey('visitor.id'))

    # BACK POPULATE
    visitor: Mapped['Visitor'] = relationship(back_populates='passages')


class ApprovalComments(SqlAlchemyBase):
    __tablename__ = 'approval_comments'
    id: Mapped[primary_key]
    request_id: Mapped[int] = mapped_column(ForeignKey('request_main.id'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    request_status_id: Mapped[int] = mapped_column(ForeignKey('request_status.id'))
    comment: Mapped[str]

    # BACK POPULATE
    status: Mapped['RequestStatus'] = relationship()
    request: Mapped['RequestMain'] = relationship(back_populates='approval_comments')
    user: Mapped['UserModel'] = relationship(back_populates='approval_comments')
