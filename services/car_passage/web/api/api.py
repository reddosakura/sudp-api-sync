import datetime
from datetime import time
from typing import List, Optional
from fastapi import APIRouter
from starlette import status

from car_passage.car_passage_service.car_passage_service import CarPassageService
from car_passage.repository.car_passage_repository import CarPassageRepository
from car_passage.repository.database_unit import DatabaseUnit
from .schemas import CarPassageSchema, ListCarPassageSchema, CarPassageBaseSchema


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/passage/get/{car_passage_id}", response_model=CarPassageSchema)
def get_car_passage(car_passage_id: int):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = CarPassageRepository(unit.session)
            car_passage_service = CarPassageService(repo)
            result = car_passage_service.get_car_passage(car_passage_id)

    return result


@router.get("/passage/search", response_model=ListCarPassageSchema)
def search_car_passage(value: Optional[str],
                       ftime: time,
                       ttime: time,
                       fdate: datetime.datetime = datetime.datetime.now().date(),
                       tdate: datetime.datetime = datetime.datetime.now().date()):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = CarPassageRepository(unit.session)
            car_passage_service = CarPassageService(repo)
            results = car_passage_service.search_car_passage(value, tdate, fdate, ftime, ttime)
    return {
        "c_passages": [result.to_dict() for result in results],
    }

@router.get("/passage/list", response_model=ListCarPassageSchema)
def list_car_passage(
        ftime: time,
        ttime: time,
        fdate: datetime.datetime = datetime.datetime.now().date(),
        tdate: datetime.datetime = datetime.datetime.now().date(),
):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = CarPassageRepository(unit.session)
            car_passage_service = CarPassageService(repo)
            results = car_passage_service.get_car_passage_list(fdate, tdate, ftime, ttime)
    return {
        "c_passages": [result.to_dict() for result in results],
    }


@router.post("/passage/create", response_model=List[CarPassageBaseSchema])
def create_car_passage(car_passage: List[CarPassageBaseSchema]):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = CarPassageRepository(unit.session)
            car_passage_service = CarPassageService(repo)
            results = car_passage_service.create_car_passage([passage.model_dump() for passage in car_passage])
            unit.commit()
    return [result.to_dict() for result in results]

