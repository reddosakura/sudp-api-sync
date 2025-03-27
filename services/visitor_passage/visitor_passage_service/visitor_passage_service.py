from visitor_passage.repository.visitor_passage_repository import VisitorPassageRepository


class VisitorPassageService:
    def __init__(self, visitor_passage_repository: VisitorPassageRepository):
        self.visitor_passage_repository = visitor_passage_repository

    def create_visitor_passage(self, visitor_passage):
        return self.visitor_passage_repository.add(visitor_passage)

    def get_visitor_passage(self, visitor_passage_id):
        return self.visitor_passage_repository.get(visitor_passage_id)

    def search_visitor_passage(self, value, fdate, tdate):
        return self.visitor_passage_repository.search(value, fdate, tdate)
