from sqlalchemy import insert, select

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


    def list(self, fdate, tdate):
        query = select(VisitorPassageModel).where(VisitorPassageModel.pass_date.between(fdate, tdate))
        results = (self.session.execute(query)).scalars()
        return [result.to_dict() for result in results]


    def search(self, value, fdate, tdate):
        results = (self.session.execute(
            select(VisitorPassageModel)
                .join(VisitorPassageModel.visitor)
                .where(
                    (((VisitorModel.lastname.like(f'%{value.upper()}%')) |
                     ((VisitorModel.lastname.in_(value.upper().split())) &
                     (VisitorModel.name.in_(value.upper().split())) &
                     (VisitorModel.patronymic.in_(value.upper().split()))))) &
                    VisitorPassageModel.pass_date.between(fdate, tdate))
                )).scalars()
        if not results:
            raise VisitorPassageNotFound("VisitorPassage not found. Отметки о посетителя не найдены")

        return [result.to_dict() for result in results]


