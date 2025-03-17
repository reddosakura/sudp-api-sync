from sqlalchemy import insert, select

from approval_pool.approval_pool_service.approval_pool import ApprovalPool
from approval_pool.approval_pool_service.exceptions import ApprovalCommentNotFound
from approval_pool.repository.models import ApprovalCommentsModel


class ApprovalRepository:
    def __init__(self, session):
        self.session = session

    def add(self, approval_):
        payload = approval_.model_dump()
        self.session.execute(
            insert(ApprovalCommentsModel).values(payload)
        )
        return ApprovalPool(**payload)

    def get(self, id_):
        result = (self.session.execute(select(ApprovalCommentsModel).where(ApprovalCommentsModel.id == id_))).scalar()

        if not result:
            raise ApprovalCommentNotFound("Approval Comment Not Found. Пул согласования не найден")

        return ApprovalPool(**result.to_dict())


    def get_by_request_id(self, request_id):
        result = (self.session.execute(
            select(ApprovalCommentsModel).where(ApprovalCommentsModel.request_id == request_id))).scalar()

        if not result:
            raise ApprovalCommentNotFound("Approval Comment Not Found. Пул согласования не найден")

        return ApprovalPool(**result.to_dict())
