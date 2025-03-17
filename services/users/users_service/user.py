from werkzeug.security import check_password_hash

class Role:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class User:
    def __init__(self,
                 lastname, name,
                 patronymic, speciality,
                 logged_in,
                 is_deleted,
                 login=None,
                 hashed_password=None,
                 created_date=None,
                 id=None,
                 role_id=None,
                 role=None):
        self.id = id
        self.lastname = lastname
        self.name = name
        self.patronymic = patronymic
        self.role_id = role_id
        self.logged_in = logged_in
        self.login = login
        self.speciality = speciality
        self.hashed_password = hashed_password
        self.is_deleted = is_deleted
        self.created_date = created_date
        self.role_ = role

    def to_dict(self):
        return {
            'lastname': self.lastname,
            'name': self.name,
            'patronymic': self.patronymic,
            'role_id': self.role_id,
            'speciality': self.speciality,
            'role': self.role_,
            'logged_in': self.logged_in,
            'login': self.login,
            'is_deleted': self.is_deleted,
            'id': self.id,

        }

    def authenticate(self, password):
        if check_password_hash(self.hashed_password.decode('utf-8'), password):
            return {
                "authenticated": True,
                "role": self.role_["name"],
                "lnp": f"{self.lastname} {self.name} {self.patronymic}",
                "id": self.id
            }
        else:
            return {
                "authenticated": False,
                "role": None,
                "lnp": None,
                "id": None
            }
