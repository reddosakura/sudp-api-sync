import datetime
import uuid
from typing import List, Optional

from fastapi import APIRouter
from starlette import status

from requests.repository.database_unit import DatabaseUnit
from requests.repository.request_repository import RequestRepository
from requests.requests_service.requests_service import RequestsService
# from requests.repository.database_unit import DatabaseUnit
# from requests.repository.request_repository import RequestRepository
# from requests.requests_service.request import Request
# from requests.requests_service.requests_service import RequestsService
from .schemas import (
    ListRequest,
    RequestSchema,
    ListTypes,
    RequestFullCreationSchema,
    CarSchema,
    VisitorSchema, VisitorBaseSchema, CarBaseSchema, FileSchema, RequestStatusSchema, ListCarTypes, ListPassmodes,
    RequestBaseSchema, RequestFullUpdateSchema, FileBaseSchema, RequestCreatedSchema, ListVisitorsUpdateSchema, ListIds,
    ListCarsUpdateSchema
)

router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.on_event("startup")
def startup():
    with DatabaseUnit() as unit:
        unit.initialize_tables()

    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            types = request_service.get_request_types()

            if not types:
                request_service.initialize_request_types()
                unit.commit()
            else:
                print("TYPES ARE ALREADY INITIALIZED")

    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            statuses = request_service.get_request_statuses()
            if not statuses:
                request_service.initialize_request_statuses()
                unit.commit()
            else:
                print("STATUSES ARE ALREADY INITIALIZED")

    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            passmodes = request_service.get_request_passmodes()
            if not passmodes:
                request_service.initialize_request_passmodes()
                unit.commit()
            else:
                print("PASSAGE MODES ARE ALREADY INITIALIZED")

    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            transport_types = request_service.get_transport_types()
            if not transport_types:
                request_service.initialize_transport_types()
                unit.commit()
            else:
                print("TRANSPORT TYPES ARE ALREADY INITIALIZED")


@router.get("/requests/list/",
         response_model=ListRequest,
         tags=["Получение списка заявок"])
def get_list_requests(monitoring: bool = False,
                    fdate: datetime.datetime = datetime.datetime.now().date(),
                    tdate: datetime.datetime = datetime.datetime.now().date(),
                    is_filtered: bool = False,
                    is_consideration: bool = False,
                    is_approval: bool = False,
                    is_admin: bool = False,
                    creator: str = None):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.list_requests(monitoring, fdate, tdate, is_filtered, is_consideration, is_approval, is_admin, creator)

    value = [result.to_dict() for result in results]
    print(value, "<--- request_ list")

    return {
        "requests": value
    }


@router.get("/request/search", response_model=ListRequest, tags=["Поиск заявок"])
def get_search_request(value: Optional[str] = None,
                        status: Optional[str] = None,
                        is_reports: bool = False,
                        creator: Optional[str] = None,
                        fdate: datetime.datetime = datetime.datetime.now().date(),
                        tdate: datetime.datetime = datetime.datetime.now().date()):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.search_request(value, status,
                                                           is_reports, creator, fdate, tdate)

    value = [result.to_dict() for result in results]
    print(value, "<--- request_ search")
    return {
        "requests": value
    }


@router.get("/request/{request_id}", response_model=RequestSchema, tags=["Получение заявки по ID"])
def get_request(request_id: int):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.get_request(request_id)
    return result.to_dict()


@router.get("/request/car/types", response_model=ListCarTypes, tags=["Получение типов автотранспорта"])
def get_car_types():
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.get_transport_types()
    return {
        "car_types": [result.to_dict() for result in results]
    }


@router.get("/req/types", response_model=ListTypes,  tags=["Получение типов заявок"])
def get_req_types():
    print("TYPES END POINT")
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            types = request_service.get_request_types()
            value = [result.to_dict() for result in types]
    return {
        "types": value
    }


@router.get("/request/status/{name}", response_model=RequestStatusSchema, tags=["Получение статуса заявки по названию"])
def get_request_status(name: str):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.get_request_status_by_name(name)
    return result


@router.get("/request/status/id/{id}", response_model=RequestStatusSchema, tags=["Получение статуса заявки по названию"])
def get_request_status_by_id(id: uuid.UUID):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.get_request_status_by_id(id)
    return result


@router.get("/req/passmodes", response_model=ListPassmodes, tags=["Получение режимов прохода"])
def get_passmodes():
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.get_request_passmodes()
    return {
        "passage_modes": [result.to_dict() for result in results]
    }


@router.get("/request/car/{car_id}", response_model=CarSchema, tags=["Получение автотранспорта по ID"])
def get_car(car_id: uuid.UUID):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.get_car(car_id)
    return result.to_dict()


@router.get("/request/cars/on_territory", response_model=List[CarSchema], tags=["Получение автотранспорта на территории"])
def get_cars_on_territory():
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.get_cars_on_territory()
    return [result.to_dict() for result in results]


@router.get("/request/visitor/{visitor_id}", response_model=VisitorSchema, tags=["Получение посетителя по ID"])
def get_visitor(visitor_id: uuid.UUID):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.get_visitor(visitor_id)
    return result.to_dict()


@router.post("/request/visitors/ids", response_model=ListVisitorsUpdateSchema, tags=["Получение посетителей по списку ID"])
def get_visitors_for_update(payload: ListIds):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.get_visitors_with_ids(payload.ids)
    return {
        "visitors": [result.to_dict() for result in results]
    }

@router.post("/request/cars/ids", response_model=ListCarsUpdateSchema, tags=["Получение автотранспорта по списку ID"])
def get_cars_for_update(payload: ListIds):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            results = request_service.get_cars_with_ids(payload.ids)
    return {
        "cars": [result.to_dict() for result in results]
    }


@router.post("/request/create", response_model=RequestCreatedSchema, tags=["Создание заявок"])
def create_request(payload: RequestFullCreationSchema):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.create_request(**payload.model_dump())
            unit.commit()

    return result

@router.post("/request/create/visitors", response_model=List[VisitorBaseSchema], tags=["Создание посетителей"])
def create_visitors(payload: List[VisitorBaseSchema]):
    print(payload)
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.create_visitors([visitor.model_dump() for visitor in payload])
            unit.commit()

    return result


@router.post("/request/create/cars", response_model=List[CarSchema], tags=["Создание автотранспорта"])
def create_cars(payload: List[CarBaseSchema]):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.create_cars([car.model_dump() for car in payload])
            unit.commit()

    return result


@router.post("/request/create/files", response_model=List[FileBaseSchema], tags=["Создание файлов"])
def create_request(payload: List[FileBaseSchema]):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            result = request_service.create_files([file.model_dump() for file in payload])
            unit.commit()

    return result

@router.put("/request/update", status_code=status.HTTP_204_NO_CONTENT, tags=["Редактирование заявок"])
def update_request(payload: RequestFullUpdateSchema):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = RequestRepository(unit.session)
            request_service = RequestsService(repo)
            request_service.update_request(**payload.model_dump())
            unit.commit()
