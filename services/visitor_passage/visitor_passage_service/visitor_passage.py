import httpx


class VisitorPassage:
    def __init__(self, pass_date, status, visitor_id, visitor=None, id=None):
        self.id = id
        self.pass_date = pass_date
        self.status = status
        self.visitor_id = visitor_id
        self.visitor = visitor

    def get_visitor(self):
        timeout = httpx.Timeout(10.0, read=None)
        print(self.visitor_id, "<<-- visitor_id")
        with httpx.Client() as client:
            response = client.get(
                f"http://requestapi/api/v3/request/visitor/{self.visitor_id}",
                headers={
                    "accept": "application/json",
                    # "Authorization": f"Bearer {access_token}",
                },
                timeout=timeout
            )
            print(response.status_code, "<-- status code")
        return response.json()

    def to_dict(self):
        return {
            'id': self.id,
            'pass_date': self.pass_date,
            'status': self.status,
            'visitor_id': self.visitor_id,
            'visitor': self.get_visitor()
        }
