from enum import Enum


# class RequestType(Enum):
#     REUSABLE = "Многоразовая"
#     DISPOSABLE = "Одноразовая"
#
#
# class Value(Enum):
#     DEFAULT = 1


class RequestStatusEnum(Enum):
    APPROVE = "Согласование"
    ALLOWED = "Одобрена"
    REJECTED = "Отклонена"
    WITHDRAWN = "Отозвана"
    CONSIDERATION = "Рассмотрение"
    CLOSED = "Закрыта"
    PASSAPPROVAL = "Прошла согласование"
    UNPASSAPPROVAL = "Не прошла согласование"


class PassmodesEnum(Enum):
    ALLDAYS = "По всем дням"
    WEEKDAYS_ONLY = "Только по будням"
    WEEKENDS_ONLY = "Только по выходным"

#
# class PassageReportsMode(str, Enum):
#     CARS = "Автомобили"
#     VISITORS = "Посетители"
#     SPEC_TRANSPORT = "Спецтранспорт"
#     SEARCH_CAR = "ПОИСК"
#     SEARCH_VISITOR = "ПОИСК"
#     SEARCH_SPECTRANSPORT = "ПОИСК"
#
#
# class OnTerritoryMode(str, Enum):
#     CARS = "Автомобили"
#     SPEC_TRANSPORT = "Спецтранспорт"
#
#
# class Scopes(Enum):
#     SUPERUSER = "superuser"
#     ADMIN = "admin"
#     LIMITED_ADMIN = "limited_admin"
#     REQUESTER = "requester"
#     MONITORING = "monitoring"
#     CURRENT = "current_user"
