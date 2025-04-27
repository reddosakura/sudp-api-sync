import httpx

from requests.requests_service.exceptions import UserApiInvalidException


class RequestType:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name
        }

class RequestStatus:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class PassageMode:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class File:
    def __init__(self,  path, request_id=None, request_=None, id=None):
        self.id = id
        self.path = path
        self.request_id = request_id
        self.request_ = request_

    def to_dict(self):
        return {
            "id": self.id,
            "path": self.path,
            "request_id": self.request_id
        }


class Visitor:

    def __init__(self,
                 lastname,
                 name,
                 patronymic,
                 passed_status,
                 is_deleted,
                 request_id=None,
                 date_deleted=None,
                 date_created=None,
                 request_=None, id=None, passages=None):

        self.id = id
        self.lastname = lastname
        self.name = name
        self.patronymic = patronymic
        self.request_id = request_id
        self.passed_status = passed_status
        self.is_deleted = is_deleted
        self.date_deleted = date_deleted
        self.date_created = date_created
        self.request_ = request_
        self.passages = passages

    def to_dict(self):
        return {
            'id': self.id,
            'lastname': self.lastname,
            'name': self.name,
            'patronymic': self.patronymic,
            'request_id': self.request_id,
            'passed_status': self.passed_status,
            'is_deleted': self.is_deleted,
            'date_deleted': self.date_deleted,
            'date_created': self.date_created
        }


class TransportType:
    def __init__(self, id, type, cars=None):
        self.id = id
        self.type = type
        self.cars = cars

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type
        }


class Car:
    def __init__(self,
                 govern_num,
                 car_model,
                 passed_status,
                 type_id,
                 visitor_id,
                 is_deleted,
                 on_territory,
                 request_id=None,
                 date_deleted=None,
                 date_created=None,id=None,
                 transport_type=None, driver=None):
        self.id = id
        self.govern_num = govern_num
        self.car_model = car_model
        self.passed_status = passed_status
        self.type_id = type_id
        self.request_id = request_id
        self.visitor_id = visitor_id
        self.is_deleted = is_deleted
        self.on_territory = on_territory
        self.date_deleted = date_deleted
        self.date_created = date_created
        self.transport_type = transport_type
        self.driver = driver

    def to_dict(self):
        return {
            "id": self.id,
            "govern_num": self.govern_num,
            "car_model": self.car_model,
            "passed_status": self.passed_status,
            "type_id": self.type_id,
            "request_id": self.request_id,
            "visitor_id": self.visitor_id,
            "is_deleted": self.is_deleted,
            "on_territory": self.on_territory,
            "date_deleted": self.date_deleted,
            "date_created": self.date_created,
            "driver": self.driver if self.driver else None,
            "transport_type": self.transport_type if self.transport_type else None,
        }


class Request:

    def __init__(self, type_id,
                 date_created,
                 contract_name, organization,
                 from_date, to_date,
                 from_time, to_time,
                 comment, request_status_id,
                 passmode_id, creator, is_deleted, id=None,
                 visitors=None, cars=None,
                 request_type=None, passmode=None,
                 status=None, files=None
                 ):
        self.creator_ = None
        self.id = id
        self.date_created = date_created
        self.type_id = type_id
        self.contract_name = contract_name
        self.organization = organization
        self.from_date = from_date
        self.to_date = to_date
        self.from_time = from_time
        self.to_time = to_time
        self.comment = comment
        self.files_ = files
        self.request_status_id = request_status_id
        self.passmode_id = passmode_id
        self.creator = creator
        self.is_deleted = is_deleted
        self.visitors_ = visitors
        self.cars_ = cars
        self.type_ = request_type
        self.status_ = status
        self.passmode_ = passmode
        # self.approval_comments_ = approval_comments
        # self.creator_ = creatorobj
        self.timeout = httpx.Timeout(10.0, read=None)


    def get_creator(self):
        url = "http://userapi/api/v3/users/" + str(self.creator)
        print(url)
        with httpx.Client() as client:
            response = client.get(
                url,
                headers={
                    "accept": "application/json",
                },
                timeout=self.timeout
            )
            if response.status_code != 200:
                raise UserApiInvalidException("User API returned invalid code. Сервис пользователей вернул неверный код")
        return response.json()


    def get_approval(self):
        url = f"http://apprpoolapi/api/v3/approval/request/{self.id}"
        print(url)
        with httpx.Client() as client:
            response = client.get(
                url,
                headers={
                    "accept": "application/json",
                    # "Authorization": f"Bearer {access_token}",
                },
                timeout=self.timeout
            )
            if response.status_code != 200:
                return {}
        return response.json()



    def to_dict(self):
        return {
            "id": self.id,
            "date_created": self.date_created,
            "type_id": self.type_id,
            "contract_name": self.contract_name,
            "organization": self.organization,
            "from_date": self.from_date,
            "to_date": self.to_date,
            "from_time": self.from_time,
            "to_time": self.to_time,
            "comment": self.comment,
            "request_status_id": self.request_status_id,
            "passmode_id": self.passmode_id,
            "creator": self.creator,
            "is_deleted": self.is_deleted,
            "files": [f for f in self.files_] if self.files_ else None,
            "visitors": [v for v in self.visitors_] if self.visitors_ else None,
            "cars": [c for c in self.cars_]  if self.cars_ else None,
            "type": self.type_ if self.type_ else None,
            "status": self.status_.to_dict() if self.status_ else None,
            "passmode": self.passmode_.to_dict() if self.passmode_ else None,
            "creatorobj": self.get_creator(),
            "approval": self.get_approval()
            # "files": [f for f in self.files_] if self.files_ else None,
            # "visitors": [v.to_dict() for v in self.visitors_] if self.visitors_ else None,
            # "cars": [c.to_dict() for c in self.cars_] if self.cars_ else None,
            # "type": self.type_.to_dict() if self.type_ else None,
            # "status": self.status_.to_dict() if self.status_ else None,
            # "passmode": self.passmode_.to_dict() if self.passmode_ else None,
        }
