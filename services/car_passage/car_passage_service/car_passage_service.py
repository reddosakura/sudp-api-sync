from car_passage.repository.car_passage_repository import CarPassageRepository


class CarPassageService:
    def __init__(self, car_passage_repository: CarPassageRepository):
        self.car_passage_repository = car_passage_repository

    def create_car_passage(self, car_passage):
        return self.car_passage_repository.add(car_passage)

    def get_car_passage(self, car_passage_id):
        return self.car_passage_repository.get(car_passage_id)

    def search_car_passage(self, value, fdate, tdate):
        return self.car_passage_repository.search(value, fdate, tdate)
