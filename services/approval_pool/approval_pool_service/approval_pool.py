import httpx


class ApprovalPool:
    def __init__(self,  request_id, user_id, request_status_id, comment, created_date, status=None, id=None):
        self.id = id
        self.request_id = request_id
        self.user_id = user_id
        self.request_status_id = request_status_id
        self.created_date = created_date
        self.comment = comment
        self.status = status

    def get_user(self):
        timeout = httpx.Timeout(10.0, read=None)
        with httpx.Client() as client:
            response = client.get(
                f"http://userapi/api/v3/users/{self.user_id}/",
                headers={
                    "accept": "application/json",
                    # "Authorization": f"Bearer {access_token}",
                },
                timeout=timeout
            )
        return response.json()


    def to_dict(self):
        return {
            "id": self.id,
            "request_id": self.request_id,
            "user_id": self.user_id,
            "request_status_id": self.request_status_id,
            "comment": self.comment,
            "created_date": self.created_date,
        }

