from .exceptions import ApprovalCommentNotFound
from approval_pool.repository.approval_repository import ApprovalRepository


class ApprovalPoolService:
    def __init__(self, approval_repository: ApprovalRepository):
        self.approval_repository = approval_repository

    def get_approval_pool(self, approval_pool_id):
        return self.approval_repository.get(approval_pool_id)

    def get_approval_by_id(self, request_id):
        approval_pool = self.approval_repository.get_by_request_id(request_id)
        if approval_pool is None:
            raise ApprovalCommentNotFound("Approval pool not found. Пул согласования не найден")
        return approval_pool

    def create_approval_pool(self, approval_pool):
        return self.approval_repository.add(approval_pool)

    def get_user_pool(self, request_id):
        approval_pool = self.approval_repository.get_by_request_id(request_id)
        if approval_pool is None:
            raise ApprovalCommentNotFound("Approval pool not found. Пул согласования не найден")

        return approval_pool.get_user()
