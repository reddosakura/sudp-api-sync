import datetime

from sqlalchemy import insert, select, cast, Time, Date
from sqlalchemy.sql import extract
from car_passage.car_passage_service.car_passage import CarPassage
from car_passage.car_passage_service.exceptions import CarPassageNotFound
from car_passage.repository.models import CarPassageModel, CarModel


class CarPassageRepository:
    def __init__(self, session):
        self.session = session

    def add(self, car_passages):
        # payload = car_passages.model_dump()
        # car_passage_list = [car.model_dump() for car in car_passages]
        self.session.execute(
            insert(CarPassageModel),
            car_passages
        )

        return [CarPassage(**car_passage) for car_passage in car_passages]

    def get(self, car_passage_id):
        result = (self.session.execute(select(CarPassageModel).where(CarPassageModel.id == car_passage_id))).scalar()
        if not result:
            raise CarPassageNotFound("CarPassage not found. Отметка о проезде не найдена")

        return result.to_dict()


    def list(self, fdate, tdate, ftime, ttime):
        query = (
            select(CarPassageModel)
                 .where(
                    (cast(CarPassageModel.pass_date, Date).between(fdate, tdate))
                    | ((cast(CarPassageModel.pass_date, Date) == tdate) & (cast(CarPassageModel.pass_date, Date) == fdate))
                )
                .where(
                    cast(CarPassageModel.pass_date, Time).between(ftime, ttime)
                )
        )
        results = (self.session.execute(query)).scalars()
        if not results:
            raise CarPassageNotFound("CarPassage not found. Отметки о проезде не найдены")
        return [CarPassage(**result.to_dict()) for result in results]


    def search(self, value, fdate, tdate, ftime, ttime):
        results = (self.session.execute(
            select(CarPassageModel)
                .join(CarPassageModel.car)
                .where(
                    ((CarModel.govern_num.like(f'%{value.upper()}%')) |
                    (CarModel.car_model.like(f'%{value.upper()}%')))
                )
                .where(
                    (cast(CarPassageModel.pass_date, Date).between(fdate, tdate))
                    | ((cast(CarPassageModel.pass_date, Date) == tdate) & (cast(CarPassageModel.pass_date, Date) == fdate))
                )
                .where(
                    cast(CarPassageModel.pass_date, Time).between(ftime, ttime)
                )
                )).scalars()
        if not results:
            raise CarPassageNotFound("CarPassage not found. Отметки о проезде не найдены")

        return [CarPassage(**result.to_dict())for result in results]


