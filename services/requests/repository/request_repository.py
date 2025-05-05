import datetime
from typing import List, Optional

import pytz
from sqlalchemy import (
    select,
    insert,
    sql,
    update, delete
)

from .enums import RequestStatusEnum, PassmodesEnum
from .models import (
    RequestMainModel,
    VisitorModel,
    CarModel,
    FileModel, RequestTypeModel,
    PassageModeModel, RequestStatusModel, TransportTypeModel, UserModel
)
from ..requests_service.exceptions import RequestNotFoundException
from ..requests_service.request import Request, Car, Visitor, PassageMode, TransportType, File, RequestStatus



class RequestRepository:
    def __init__(self, session):
        self.session = session

    def add(self, request_):
        created = self.session.scalar(
            insert(RequestMainModel).returning(RequestMainModel.id),
            request_
        )

        mapping = request_ | {"id": created}

        return Request(**mapping)


    def add_visitors(self, visitors_):
        created = self.session.scalars(
            insert(VisitorModel).returning(VisitorModel.id),
            visitors_,
        )

        list_uuids = list(created)
        mappings = [visitor | {"id": list_uuids[i]} for i, visitor in enumerate(visitors_)]

        print(mappings, "<-- mappings")

        return [Visitor(**visitor) for visitor in mappings]

    def add_cars(self, cars_):
        created = self.session.scalar(
            insert(CarModel).returning(CarModel.id),
            cars_,
        )

        return [Car(**dict(car | {"id": created})) for car in cars_]

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


    def search(self, value,
                        status: Optional[str],
                        is_reports: bool = False,
                        creator: str = None,
                        fdate: Optional[datetime.datetime] = None,
                        tdate: Optional[datetime.datetime] = None) -> List[Request]:



        query = select(RequestMainModel)

        if is_reports:
            if value:
                query = (select(RequestMainModel)
                            .join(RequestMainModel.visitors)
                            .join(RequestMainModel.cars)
                            .join(RequestMainModel.creatorobj)
                            .where(
                                (VisitorModel.lastname.like(f'%{value.upper()}%')) |
                                ((VisitorModel.lastname.in_(value.upper().split())) &
                                 (VisitorModel.name.in_(value.upper().split())) &
                                 (VisitorModel.patronymic.in_(value.upper().split()))) |
                                (RequestMainModel.organization.like(f'%{value}%')) |
                                (RequestMainModel.contract_name.like(f'%{value}%')) |
                                ((UserModel.lastname.like(f'%{value.title()}%') |
                                  UserModel.name.like(f'%{value.title()}%') |
                                  UserModel.patronymic.like(f'%{value.title()}%') |
                                  (UserModel.lastname.in_(value.title().split())) |
                                  (UserModel.name.in_(value.title().split())) |
                                  (UserModel.patronymic.in_(value.title().split())))) |
                                CarModel.govern_num.like(f'%{value.upper()}%')
                            )
                )

                if status:
                    query = query.join(RequestMainModel.status).where(RequestStatusModel.name == status)

                if fdate and tdate:
                    query = query.where((sql.func.date(RequestMainModel.from_date).between(fdate, tdate.date()))
                                        & sql.func.date(RequestMainModel.to_date).between(fdate, tdate.date()))

                query = query.distinct()

            if status:
                query = query.join(RequestMainModel.status).where(RequestStatusModel.name == status)

        if creator:
            if value:
                query = (select(RequestMainModel)
                .join(RequestMainModel.visitors)
                .join(RequestMainModel.cars)
                .where(
                    (VisitorModel.lastname.like(f'%{value.upper()}%')) |
                    ((VisitorModel.lastname.in_(value.upper().split())) &
                     (VisitorModel.name.in_(value.upper().split())) &
                     (VisitorModel.patronymic.in_(value.upper().split()))) |
                    (RequestMainModel.organization.like(f'%{value}%')) |
                    (RequestMainModel.organization.in_(value.upper().split())) |
                    (RequestMainModel.organization.match(value.upper())) |
                    (RequestMainModel.contract_name.like(f'%{value}%')) |
                    CarModel.govern_num.like(f'%{value.upper()}%')
                )
                )
                query = query.where(RequestMainModel.creator == creator).distinct()
                result = (self.session.execute(query)).scalars()
                return [Request(**data.to_dict()) for data in result]
            else:
                query = (select(RequestMainModel)
                            .where(RequestMainModel.creator == creator)
                            .where((datetime.datetime.now().date().today() >= RequestMainModel.from_date)
                                & ((RequestMainModel.to_date >= datetime.datetime.now().date().today())
                                   | (RequestMainModel.from_date > datetime.datetime.now().today()))
                            )
                         .distinct())

        if fdate and tdate:
            query = query.where((sql.func.date(RequestMainModel.from_date).between(fdate, tdate))
                                                   & sql.func.date(RequestMainModel.to_date).between(fdate, tdate))

        result = (self.session.execute(query)).scalars()

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
                    is_archived: bool = False,
                    creator: str = None):
        # query = select(RequestMainModel).where((fdate <= RequestMainModel.from_date)
        #                                    & (RequestMainModel.to_date <= tdate))

        query = (select(RequestMainModel)
                            .where((datetime.datetime.now().date().today() >= RequestMainModel.from_date)
                                & ((RequestMainModel.to_date >= datetime.datetime.now().date().today())
                                   | (RequestMainModel.from_date > datetime.datetime.now().today()))
                            )
                         .distinct().order_by(RequestMainModel.date_created))
        if is_filtered:
            query = select(RequestMainModel).where((sql.func.date(RequestMainModel.from_date).between(fdate, tdate))
                                               & sql.func.date(RequestMainModel.to_date).between(fdate, tdate))
        if monitoring:
            query = (
                select(RequestMainModel)
                    .join(RequestMainModel.status)
                    .join(RequestMainModel.passmode)
                    .where(
                        (datetime.datetime.now().date().today() >= RequestMainModel.from_date)
                        & ((RequestMainModel.to_date >= datetime.datetime.now().date().today())
                        | (RequestMainModel.from_date > datetime.datetime.now().today()))
                    )
                    .where(
                        (datetime.datetime.now(pytz.timezone("Europe/Moscow")).time() >= RequestMainModel.from_time)
                        & (RequestMainModel.to_time > datetime.datetime.now(pytz.timezone("Europe/Moscow")).time())
                    )
                    .where(
                        ((PassageModeModel.name == PassmodesEnum.WEEKENDS_ONLY.value) & (datetime.datetime.now().date().weekday() in [5, 6]))
                        | (PassageModeModel.name == PassmodesEnum.ALLDAYS.value)
                        | ((PassageModeModel.name == PassmodesEnum.WEEKDAYS_ONLY.value) & (datetime.datetime.now().date().weekday() < 5))
                    )
                    .where(
                        (RequestStatusModel.name == RequestStatusEnum.ALLOWED.value)
                    )
             )
        if is_consideration:
            query = select(RequestMainModel).join(RequestMainModel.status).where(RequestStatusModel.name == RequestStatusEnum.CONSIDERATION.value)

        if is_approval:
            query = select(RequestMainModel).join(RequestMainModel.status).where(RequestStatusModel.name == RequestStatusEnum.APPROVE.value)

        if is_admin:
            query = (select(RequestMainModel).join(RequestMainModel.status)
                        .where(
                            (RequestStatusModel.name == RequestStatusEnum.PASSAPPROVAL.value) |
                            (RequestStatusModel.name == RequestStatusEnum.APPROVE.value))
            )


        if creator:
            query = query.where(RequestMainModel.creator == creator)

        if creator and is_archived:
            query = (select(RequestMainModel)
                     .where(RequestMainModel.creator == creator)
                     .where(RequestMainModel.to_date < fdate)
                     )

        results = (self.session.execute(query)).scalars()

        if not results:
            raise RequestNotFoundException("Request not found. Заявка не найдена")
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

    def get_status_by_id(self, id):
        result = (self.session.execute(
            select(RequestStatusModel)
                .where(RequestStatusModel.id == id)
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

        return Car(**result.to_dict())

    def get_cars_with_ids(self, list_ids):
        results = (self.session.execute(
            select(CarModel).where(CarModel.id.in_(list_ids))
        )).scalars()

        return [Car(**result.to_dict()) for result in results]

    def get_cars_on_territory(self):
        results = (self.session.execute(
            select(CarModel).where(CarModel.on_territory == True)
        )).scalars()

        return [Car(**result.to_dict()) for result in results]

    def get_visitor(self, visitor_id):
        result = (self.session.execute(
            select(VisitorModel).where(VisitorModel.id == visitor_id)
        )).scalar()

        return Visitor(**result.to_dict())

    def get_visitors_with_ids(self, list_ids):
        results = (self.session.execute(
            select(VisitorModel).where(VisitorModel.id.in_(list_ids))
        )).scalars()

        return [Visitor(**result.to_dict()) for result in results]

    def update(self, request_payload, visitors_payload, cars_payload, files_payload):
        if request_payload:
            self.session.execute(
                update(RequestMainModel)
                      .where(RequestMainModel.id == request_payload['id'])
                      .values(request_payload)
            )

        if visitors_payload:
            self.session.execute(
                update(VisitorModel),
                [visitor for visitor in visitors_payload]
            )

        if cars_payload:
            self.session.execute(
                update(CarModel),
                [car for car in cars_payload]
            )

        if files_payload:
            self.session.execute(
                delete(FileModel).where(FileModel.request_id == request_payload['id'])
            )

            self.session.execute(
                insert(FileModel),
                files_payload
            )


        if request_payload:
            return Request(**request_payload)
        elif visitors_payload:
            [Visitor(**visitor) for visitor in visitors_payload]
        elif cars_payload:
            [Car(**car) for car in cars_payload]

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
