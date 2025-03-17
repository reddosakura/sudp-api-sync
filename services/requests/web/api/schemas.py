import datetime
import uuid
from typing import Optional, List

from pydantic import BaseModel


class RequestTypeSchema(BaseModel):
    id: uuid.UUID
    name:str

    class Config:
        from_attributes = True


class RequestStatusSchema(BaseModel):
    id: uuid.UUID
    name:str

    class Config:
        from_attributes = True


class PassageModeSchema(BaseModel):
    id: uuid.UUID
    name:str

    class Config:
        from_attributes = True


class FileBaseSchema(BaseModel):
    path: str
    request_id: int

    class Config:
        from_attributes = True


class FileSchema(FileBaseSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True


class VisitorBaseSchema(BaseModel):
    lastname: str
    name: str
    patronymic: str
    request_id: int
    passed_status: bool
    is_deleted: bool
    date_deleted: Optional[datetime.datetime]
    date_created: Optional[datetime.datetime] = datetime.datetime.now()

    class Config:
        from_attributes = True


class VisitorUpdateSchema(BaseModel):
    id: uuid.UUID
    lastname: str
    name: str
    patronymic: str
    passed_status: bool
    is_deleted: bool

    class Config:
        from_attributes = True
#


class VisitorSchema(VisitorBaseSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True


class TransportTypeSchema(BaseModel):
    id: uuid.UUID
    type: str

    class Config:
        from_attributes = True


class CarBaseSchema(BaseModel):
    govern_num: str
    car_model: str
    passed_status: bool
    type_id: uuid.UUID
    request_id: int
    visitor_id: Optional[uuid.UUID]
    is_deleted: bool
    date_deleted: Optional[datetime.datetime]
    date_created: Optional[datetime.datetime] = datetime.datetime.now()

    class Config:
        from_attributes = True


class CarUpdateSchema(BaseModel):
    id: uuid.UUID
    govern_num: str
    car_model: str
    passed_status: bool
    type_id: uuid.UUID
    # request_id: int
    visitor_id: Optional[uuid.UUID]
    is_deleted: bool

    class Config:
        from_attributes = True


class CarSchema(CarBaseSchema):
    id: uuid.UUID
    visitor_: Optional[VisitorSchema] = None
    transport_type: TransportTypeSchema

    class Config:
        from_attributes = True



class RequestSchema(BaseModel):
    id: int
    type_id: uuid.UUID
    contract_name: str
    organization: str
    from_date: datetime.datetime
    to_date: datetime.datetime
    from_time: datetime.time
    to_time: datetime.time
    comment: str
    request_status_id: uuid.UUID
    passmode_id: uuid.UUID
    creator: uuid.UUID
    is_deleted: bool
    files: Optional[List[FileSchema]]
    visitors: Optional[List[VisitorSchema]]
    cars: Optional[List[CarSchema]]
    type: RequestTypeSchema
    status: RequestStatusSchema
    passmode: PassageModeSchema
    # creator: dict

    class Config:
        from_attributes = True


class RequestBaseSchema(BaseModel):
    type_id: uuid.UUID
    contract_name: str
    organization: str
    from_date: datetime.datetime
    to_date: datetime.datetime
    from_time: datetime.time
    to_time: datetime.time
    comment: str
    request_status_id: uuid.UUID
    passmode_id: uuid.UUID
    creator: uuid.UUID
    is_deleted: bool

    class Config:
        from_attributes = True


class RequestCreatedSchema(RequestBaseSchema):
    id: int
    class Config:
        from_attributes = True


class RequestFullCreationSchema(BaseModel):
    request_: RequestBaseSchema
    # visitors_: Optional[List[VisitorBaseSchema]]
    # cars_: Optional[List[CarBaseSchema]]
    # files_: Optional[List[FileSchema]]

    class Config:
        from_attributes = True


class RequestFullUpdateSchema(BaseModel):
    # request_: RequestUpdateSchema
    request_: RequestBaseSchema
    visitors_: Optional[List[VisitorUpdateSchema]]
    cars_: Optional[List[CarUpdateSchema]]
    # files_: Optional[List[FileSchema]]

    class Config:
        from_attributes = True



class ListRequest(BaseModel):
    requests: List[RequestSchema]


class ListTypes(BaseModel):
    types: List[RequestTypeSchema]


class ListCarTypes(BaseModel):
    car_types: List[TransportTypeSchema]


class ListPassmodes(BaseModel):
    passage_modes: List[PassageModeSchema]
