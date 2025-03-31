from importlib.metadata import files

from ..repository.request_repository import RequestRepository
from .exceptions import RequestNotFoundException


class RequestsService:
    def __init__(self, request_repository: RequestRepository):
        self.request_repository = request_repository

    def get_request(self, request_id):
        return self.request_repository.get(request_id)

    def list_requests(self, monitoring, fdate, tdate, is_filtered, is_consideration, is_approval, is_admin, creator_id):
        return self.request_repository.list(monitoring, fdate, tdate, is_filtered, is_consideration, is_approval, is_admin, creator_id)

    def search_request(self, value, status, is_reports, creator, fdate, tdate):
        return self.request_repository.search(value, status, is_reports, creator, fdate, tdate)

    def create_request(self, request_):
        return self.request_repository.add(request_)

    def create_visitors(self, visitors_):
        return self.request_repository.add_visitors(visitors_)

    def create_cars(self, cars_):
        return self.request_repository.add_cars(cars_)

    def create_files(self, files_):
        return self.request_repository.add_files(files_)

    def update_request(self, request_, visitors_, cars_):
        if request_:
            request = self.request_repository.get(request_['id'])
            if not request:
                raise RequestNotFoundException("Request not found. Заявка не найдена")

        return self.request_repository.update(request_, visitors_, cars_)

    def get_request_types(self):
        types = self.request_repository.get_all_types()
        return types

    def get_request_passmodes(self):
        return self.request_repository.get_all_passmodes()

    def get_request_statuses(self):
        return self.request_repository.get_all_statuses()

    def get_request_status_by_name(self, name):
        return self.request_repository.get_status_by_name(name)
    def get_request_status_by_id(self, id):
        return self.request_repository.get_status_by_name(id)

    def get_transport_types(self):
        return self.request_repository.get_all_transport_types()

    def get_car(self, car_id):
        return self.request_repository.get_car(car_id)

    def get_cars_with_ids(self, list_ids):
        return self.request_repository.get_cars_with_ids(list_ids)

    def get_cars_on_territory(self):
        return self.request_repository.get_cars_on_territory()

    def get_visitor(self, visitor_id):
        return self.request_repository.get_visitor(visitor_id)

    def get_visitors_with_ids(self, list_ids):
        return self.request_repository.get_visitors_with_ids(list_ids)

    def initialize_request_types(self):
        return self.request_repository.initialize_req_types()

    def initialize_request_passmodes(self):
        return self.request_repository.initialize_req_passmodes()

    def initialize_request_statuses(self):
        return self.request_repository.initialize_req_statuses()

    def initialize_transport_types(self):
        return self.request_repository.initialize_transport_types()
