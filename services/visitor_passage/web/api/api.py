import datetime
from typing import List
from fastapi import APIRouter
from visitor_passage.visitor_passage_service.visitor_passage_service import VisitorPassageService
from visitor_passage.repository.visitor_passage_repository import VisitorPassageRepository
from visitor_passage.repository.database_unit import DatabaseUnit
from .schemas import VisitorPassageSchema, ListVisitorPassageSchema, VisitorPassageBaseSchema


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get("/passage/get/{visitor_passage_id}", response_model=VisitorPassageSchema)
async def get_visitor_passage(visitor_passage_id: int):
    async with DatabaseUnit() as unit:
        async with unit.session.begin():
            repo = VisitorPassageRepository(unit.session)
            visitor_passage_service = VisitorPassageService(repo)
            result = await visitor_passage_service.get_visitor_passage(visitor_passage_id)

    return result.to_dict()


@router.get("/passage/search", response_model=ListVisitorPassageSchema)
async def search_visitor_passage(value: str, fdate: datetime.datetime = datetime.datetime.now().date(),
                             tdate: datetime.datetime = datetime.datetime.now().date()):
    async with DatabaseUnit() as unit:
        async with unit.session.begin():
            repo = VisitorPassageRepository(unit.session)
            visitor_passage_service = VisitorPassageService(repo)
            results = await visitor_passage_service.search_visitor_passage(value, tdate, fdate)
    return {
        "v_passages": [result.to_dict() for result in results],
    }


@router.post("/passage/create", response_model=List[VisitorPassageBaseSchema])
async def create_visitor_passage(visitor_passages: List[VisitorPassageBaseSchema]):
    async with DatabaseUnit() as unit:
        async with unit.session.begin():
            repo = VisitorPassageRepository(unit.session)
            visitor_passage_service = VisitorPassageService(repo)
            results = await visitor_passage_service.create_visitor_passage([visitor_passage.model_dump() for visitor_passage in visitor_passages])
            await unit.commit()
    return [result.to_dict() for result in results]

