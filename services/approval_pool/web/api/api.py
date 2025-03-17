import uuid
from fastapi import APIRouter
from approval_pool.approval_pool_service.approval_pool import ApprovalPool
from approval_pool.approval_pool_service.approval_pool_service import ApprovalPoolService
from approval_pool.repository.approval_repository import ApprovalRepository
from approval_pool.repository.database_unit import DatabaseUnit
from .schemas import ApprovalSchema, ApprovalBaseSchema


router = APIRouter(
    responses={404: {"description": "Not found"}},
)


@router.get('/approval/user/{request_id}')
def get_user_approval(request_id: int):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = ApprovalRepository(unit.session)
            approval_service = ApprovalPoolService(repo)
            result = approval_service.get_user_pool(request_id)
    return result



@router.get('/approval/request/{request_id}', response_model=ApprovalSchema)
def get_approval_from_request(request_id: int):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = ApprovalRepository(unit.session)
            approval_service = ApprovalPoolService(repo)
            result = approval_service.get_approval_by_id(request_id)

    return result.to_dict()


@router.get('/approval/{approval_id}', response_model=ApprovalSchema)
def get_approval(approval_id: uuid.UUID):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = ApprovalRepository(unit.session)
            approval_service = ApprovalPoolService(repo)
            result = approval_service.get_approval_by_id(approval_id)
    return result.to_dict()


@router.post('/approval/create/')
def create_approval(approval_: ApprovalBaseSchema):
    with DatabaseUnit() as unit:
        with unit.session.begin():
            repo = ApprovalRepository(unit.session)
            approval_service = ApprovalPoolService(repo)
            result = approval_service.create_approval_pool(approval_)
            unit.commit()

    return result.to_dict()
