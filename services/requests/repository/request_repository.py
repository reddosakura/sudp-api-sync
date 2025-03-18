import datetime
from typing import List

from sqlalchemy import (
    select,
    insert,
    sql,
    union_all,
    update
)

from .enums import RequestStatusEnum
from .models import (
    RequestMainModel,
    VisitorModel,
    CarModel,
    FileModel, RequestTypeModel,
    PassageModeModel, RequestStatusModel, TransportTypeModel
)
from ..requests_service.exceptions import RequestNotFoundException
from ..requests_service.request import Request, RequestType, Car, Visitor, PassageMode, TransportType, File, RequestStatus


class RequestRepository:
    def __init__(self, session):
        self.session = session

    def add(self, request_):
        created = self.session.scalar(
            insert(RequestMainModel).returning(RequestMainModel.id)
                ,request_
        )

        print(request_ | {"id": created}, "<-- request_schema")
        mapping = request_ | {"id": created}

        return Request(**mapping)


    def add_visitors(self, visitors_):
        self.session.execute(
            insert(VisitorModel),
            visitors_,
        )

        return [Visitor(**visitor) for visitor in visitors_]

    def add_cars(self, cars_):
        self.session.execute(
            insert(CarModel),
            cars_,
        )
        return [Car(**car) for car in cars_]

    def add_files(self, files_):
        self.session.execute(
            insert(FileModel),
            files_
        )

        return [File(**file) for file in files_]

    def get(self, request_id):
        result = (self.session.execute(select(RequestMainModel).where(RequestMainModel.id == request_id))).scalar()
        if not result:
            raise RequestNotFoundException("Request not found. Заявка не найдена")
        return Request(**result.to_dict())


    def search(self, value, monitoring: bool = False,
                        is_filtered: bool = False,
                        is_reports: bool = False,
                        creator: str = None,
                        fdate: datetime.datetime = datetime.datetime.now().date(),
                        tdate: datetime.datetime = datetime.datetime.now().date()) -> List[Request]:

        query_v = select(RequestMainModel).join(RequestMainModel.visitors).where(
            (VisitorModel.lastname.like(f'%{value.upper()}%')) |
            ((VisitorModel.lastname.in_(value.upper().split())) &
             (VisitorModel.name.in_(value.upper().split())) &
             (VisitorModel.patronymic.in_(value.upper().split()))) |
            (RequestMainModel.organization.like(f'%{value}%')) |
            (RequestMainModel.organization.in_(value.upper().split())) |
            (RequestMainModel.organization.match(value.upper())) |
            (RequestMainModel.contract_name.like(f'%{value}%'))
        )
        query_c = select(RequestMainModel).join(RequestMainModel.cars).where(
            CarModel.govern_num.like(f'%{value.upper()}%'))

        if is_reports:
            query_v = select(RequestMainModel).join(RequestMainModel.visitors).where(
                (VisitorModel.lastname.like(f'%{value.upper()}%')) |
                ((VisitorModel.lastname.in_(value.upper().split())) &
                 (VisitorModel.name.in_(value.upper().split())) &
                 (VisitorModel.patronymic.in_(value.upper().split()))) |
                (RequestMainModel.organization.like(f'%{value}%')) |
                (RequestMainModel.organization.in_(value.upper().split())) |
                (RequestMainModel.organization.match(value.upper())) |
                (RequestMainModel.contract_name.like(f'%{value}%')) |
                (RequestMainModel.creator.like(f'%{value.title()}%'))
            )
            query_c = select(RequestMainModel).join(RequestMainModel.cars).where(
                CarModel.govern_num.like(f'%{value.upper()}%') |
                (RequestMainModel.creator.like(f'%{value.title()}%')))

        if is_filtered:
            query_v = query_v.where((sql.func.date(RequestMainModel.from_date).between(fdate, tdate.date()))
                                    & sql.func.date(RequestMainModel.to_date).between(fdate, tdate.date()))
            query_c = query_c.where((sql.func.date(RequestMainModel.from_date).between(fdate, tdate.date()))
                                    & sql.func.date(RequestMainModel.to_date).between(fdate.date(), tdate.date()))

        if monitoring:
            query_v = query_v.where(((datetime.datetime.now().date().today() >= RequestMainModel.from_date)
                                     & (RequestMainModel.to_date >= datetime.datetime.now().date().today())
                                     | (RequestMainModel.from_date > datetime.datetime.now().today()))
                                    & (RequestMainModel.status == RequestStatusEnum.ALLOWED.value)
                                    )

            query_c = query_c.where(((datetime.datetime.now().date().today() >= RequestMainModel.from_date)
                                     & (RequestMainModel.to_date >= datetime.datetime.now().date().today())
                                     | (RequestMainModel.from_date > datetime.datetime.now().today()))
                                    & (RequestMainModel.status == RequestStatusEnum.ALLOWED.value))

        if creator:
            query_v = query_v.where(RequestMainModel.creator == creator)
            query_c = query_c.where(RequestMainModel.creator == creator)

        union_query = select(RequestMainModel).from_statement(union_all(query_v, query_c))

        result = (self.session.execute(union_query)).scalars()

        if not result:
            raise RequestNotFoundException("Request not found. Заявка не найдена")

        return [Request(**data.to_dict()) for data in result]

    def list(self,
                    monitoring: bool = False,
                    fdate: datetime.datetime = datetime.datetime.now().date(),
                    tdate: datetime.datetime = datetime.datetime.now().date(),
                    is_filtered: bool = False,
                    is_consideration: bool = False,
                    is_approval: bool = False,
                    is_admin: bool = False,
                    creator: str = None):
        query = select(RequestMainModel).where((fdate >= RequestMainModel.from_date)
                                           & (RequestMainModel.to_date >= tdate)
                                           | (RequestMainModel.from_date > fdate))
        if is_filtered:
            query = select(RequestMainModel).where((sql.func.date(RequestMainModel.from_date).between(fdate, tdate))
                                               & sql.func.date(RequestMainModel.to_date).between(fdate, tdate))
        if monitoring:
            query = select(RequestMainModel).where((datetime.datetime.now().date().today() >= RequestMainModel.from_date)
                                               & (RequestMainModel.to_date >= datetime.datetime.now().date().today())
                                               | (RequestMainModel.from_date > datetime.datetime.now().today())
                                               ).where((RequestMainModel.status == RequestStatusEnum.ALLOWED.value))
        if is_consideration:
            query = select(RequestMainModel).join(RequestMainModel.request_type).where((fdate >= RequestMainModel.from_date)
                                           & (RequestMainModel.to_date >= tdate)
                                           | (RequestMainModel.from_date > fdate)).where(RequestTypeModel.name == RequestStatusEnum.CONSIDERATION.value)

        if is_approval:
            query = select(RequestMainModel).join(RequestMainModel.request_type).where((fdate >= RequestMainModel.from_date)
                                           & (RequestMainModel.to_date >= tdate)
                                           | (RequestMainModel.from_date > fdate)).where(RequestTypeModel.name == RequestStatusEnum.APPROVE.value)

        if is_admin:
            query = (select(RequestMainModel).join(RequestMainModel.request_type).where((fdate >= RequestMainModel.from_date)
                                           & (RequestMainModel.to_date >= tdate)
                                           | (RequestMainModel.from_date > fdate))
                        .where(
                            (RequestTypeModel.name == RequestStatusEnum.PASSAPPROVAL.value) |
                            (RequestTypeModel.name == RequestStatusEnum.APPROVE.value))
            )


        if creator:
            query = query.where(RequestMainModel.creator == creator).where(~RequestMainModel.is_deleted)

        results = (self.session.execute(query)).scalars()

        if not results:
            raise RequestNotFoundException("Request not found. Заявка не найдена")

        # value1 = [data.to_dict() for data in results]
        #
        # print(value1, "<--- request_ list repo")
        value = [Request(**data.to_dict()) for data in results]

        return value

    def get_all_types(self):
        results = (self.session.execute(
            select(RequestTypeModel)
        )).scalars()

        return [RequestStatus(**type_.to_dict()) for type_ in results]

    def get_all_passmodes(self):
        results = (self.session.execute(
            select(PassageModeModel)
        )).scalars()

        return [PassageMode(**type_.to_dict()) for type_ in results]

    def get_all_statuses(self):
        results = (self.session.execute(
            select(RequestStatusModel)
        )).scalars()

        return [RequestStatus(**type_.to_dict()) for type_ in results]

    def get_status_by_name(self, name):
        result = (self.session.execute(
            select(RequestStatusModel)
                .where(RequestStatusModel.name == name)
        )).scalar()

        if not result:
            raise Exception("Request status not found")

        return RequestStatus(**result.to_dict())

    def get_all_transport_types(self):
        results = (self.session.execute(
            select(TransportTypeModel)
        )).scalars()

        return [TransportType(**type_.to_dict()) for type_ in results]


    def get_car(self, car_id):
        result = (self.session.execute(
            select(CarModel).where(CarModel.id == car_id)
        )).scalar()

        return Car(**result)

    def get_visitor(self, visitor_id):
        result = (self.session.execute(
            select(VisitorModel).where(VisitorModel.id == visitor_id)
        )).scalar()

        return Visitor(**result.to_dict())

    def update(self, id_, request_payload, visitors_payload, cars_payload):
        self.session.execute(
            update(RequestMainModel)
                  .where(RequestMainModel.id == id_)
                  .values(request_payload)
        )

        self.session.execute(
            update(CarModel),
            [car for car in cars_payload]
        )

        self.session.execute(
            update(VisitorModel),
            [visitor for visitor in visitors_payload]
        )

        return Request(**request_payload)

    def add_visitor_to_request(self, visitors_payload):
        self.session.execute(
            insert(VisitorModel),
            visitors_payload
        )

        return

    def add_car_to_request(self, cars_payload):
        self.session.execute(
            insert(CarModel),
            cars_payload
        )
        return

    def initialize_req_types(self):
        self.session.execute(
            insert(RequestTypeModel),
            [
                {
                    "name": "Одноразовая"
                },
                {
                    "name": "Многоразовая"
                },
            ]
        )

    def initialize_req_passmodes(self):
        self.session.execute(
            insert(PassageModeModel),
            [
                {
                    "name": "По всем дням"
                },
                {
                    "name": "Только по будням"
                },
                {
                    "name": "Только по выходным"
                },
            ]
        )

    def initialize_req_statuses(self):
        self.session.execute(
            insert(RequestStatusModel),
            [
                {
                    "name": "Согласование"
                },
                {
                    "name": "Рассмотрение"
                },
                {
                    "name": "Прошла согласование"
                },
                {
                    "name": "Не прошла согласование"
                },
                {
                    "name": "Одобрена"
                },
                {
                    "name": "Отклонена"
                },
                {
                    "name": "Отозвана"
                },
                {
                    "name": "Закрыта"
                },
            ]
        )

    def initialize_transport_types(self):
        self.session.execute(
            insert(TransportTypeModel),
            [
                {
                    "type": "По заявке"
                },
                {
                    "type": "Другое"
                },
                {
                    "type": "Скорая помощь"
                },
                {
                    "type": "Пожарная служба"
                },
                {
                    "type": "Полиция"
                },
                {
                    "type": "Газовая служба"
                },
            ]
        )
