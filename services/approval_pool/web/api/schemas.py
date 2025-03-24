import uuid
import datetime

from pydantic import BaseModel


class ApprovalBaseSchema(BaseModel):
    # id: str
    request_id: int
    user_id: uuid.UUID
    request_status_id: uuid.UUID
    comment: str
    created_date: datetime.datetime = datetime.datetime.now()

    class Config:
        from_attributes = True


class ApprovalSchema(ApprovalBaseSchema):
    id: uuid.UUID

    class Config:
        from_attributes = True
