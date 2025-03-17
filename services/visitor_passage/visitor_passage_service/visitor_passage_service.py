from visitor_passage.repository.visitor_passage_repository import VisitorPassageRepository


class VisitorPassageService:
    def __init__(self, visitor_passage_repository: VisitorPassageRepository):
        self.visitor_passage_repository = visitor_passage_repository

    async def create_visitor_passage(self, visitor_passage):
        return await self.visitor_passage_repository.add(visitor_passage)

    async def get_visitor_passage(self, visitor_passage_id):
        return await self.visitor_passage_repository.get(visitor_passage_id)

    async def search_visitor_passage(self, value, fdate, tdate):
        return await self.visitor_passage_repository.search(value, fdate, tdate)
