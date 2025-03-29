from dns.e164 import query
from sqlalchemy import insert, select, cast, Date, Time

from visitor_passage.visitor_passage_service.visitor_passage import VisitorPassage
from visitor_passage.visitor_passage_service.exceptions import VisitorPassageNotFound
from visitor_passage.repository.models import CarPassageModel, CarModel, VisitorPassageModel, VisitorModel


class VisitorPassageRepository:
    def __init__(self, session):
        self.session = session

    def add(self, visitor_passages):
        # payload = car_passage.model_dump()
        # visitors_passage_list = [visitor.model_dump() for visitor in visitor_passages]
        self.session.execute(
            insert(VisitorPassageModel),
            visitor_passages
        )

        # return VisitorPassage(**payload)
        return [VisitorPassage(**visitor_passage) for visitor_passage in visitor_passages]

    def get(self, visitor_passage_id):
        result = (self.session.execute(select(VisitorPassageModel).where(VisitorPassageModel.id == visitor_passage_id))).scalar()
        if not result:
            raise VisitorPassageNotFound("VisitorPassage not found. Отметка о проходе посетителя не найдена")

        return result.to_dict()


    def list(self, fdate, tdate, ftime, ttime):
        query_text = (
            select(VisitorPassageModel)
                 .where(
                    (cast(VisitorPassageModel.pass_date, Date).between(fdate, tdate))
                    | ((cast(VisitorPassageModel.pass_date, Date) == tdate) & (cast(VisitorPassageModel.pass_date, Date) == fdate))
                )
                .where(
                    cast(VisitorPassageModel.pass_date, Time).between(ftime, ttime)
                )
        )
        results = (self.session.execute(query_text)).scalars()
        return [VisitorPassage(**result.to_dict()) for result in results]


    def search(self, value, fdate, tdate, ftime, ttime):

        query_text = (
            select(VisitorPassageModel)
                .join(VisitorPassageModel.visitor)
                .where(
                    (VisitorModel.lastname.like(f'%{value.upper()}%')) |
                    (VisitorModel.name.like(f'%{value.upper()}%')) |
                    (VisitorModel.patronymic.like(f'%{value.upper()}%')) |
                    (((VisitorModel.lastname.in_(value.upper().split())) &
                     (VisitorModel.name.in_(value.upper().split())) &
                     (VisitorModel.patronymic.in_(value.upper().split()))))
                )
                .where(
                    (cast(VisitorPassageModel.pass_date, Date).between(fdate, tdate))
                    | ((cast(VisitorPassageModel.pass_date, Date) == tdate)
                        & (cast(VisitorPassageModel.pass_date, Date) == fdate))
                )
                .where(
                    cast(VisitorPassageModel.pass_date, Time).between(ftime, ttime)
                )
            )

        results = (self.session.execute(query_text).scalars())

        # print(list(results), "<-- sql results")

        if not results:
            raise VisitorPassageNotFound("VisitorPassage not found. Отметки о посетителя не найдены")

        return [VisitorPassage(**result.to_dict()) for result in results]
