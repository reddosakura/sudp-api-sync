import httpx


class CarPassage:
    def __init__(self, pass_date, status, car_id=None, car=None, id=None):
        self.id = id
        self.pass_date = pass_date
        self.status = status
        self.car_id = car_id
        self.car = car

    def get_car(self):
        timeout = httpx.Timeout(10.0, read=None)
        with httpx.Client() as client:
            response = client.get(
                f"http://requestapi/api/v3/request/car/{self.car_id}",
                headers={
                    "accept": "application/json",
                    # "Authorization": f"Bearer {access_token}",
                },
                timeout=timeout
            )
        return response.json()

    def to_dict(self):
        return {
            'id': self.id,
            'pass_date': self.pass_date,
            'status': self.status,
            'car_id': self.car_id,
            'car': self.get_car(),
        }
