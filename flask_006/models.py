from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from flask_006 import config
from flask_006.database import FlaskDataBase, Users


db = FlaskDataBase(config.DB_NAME, config.USER, config.PASSWORD)


def create_obj(model, obj):
    user = model(*obj[1:], is_from_db=True)
    user.set_id(obj[0])
    return user


class Model:
    table = None

    @classmethod
    def get_objs(cls, **kwargs):
        if any(kwargs):
            obj = db.get_one(cls.table, **kwargs)
            if obj:
                return create_obj(cls, obj)
            return None
        else:
            objs = db.get_all(cls.table)
            result = []
            for obj in objs:
                result.append(create_obj(cls, obj))
            return result


class UserModel(Model):
    table = Users()

    def __init__(self, email, password, created_at=None, is_from_db=False):
        self.id = None
        self.email = email

        if is_from_db:
            self.password = password
            self.created_at = created_at
        else:
            self.password = generate_password_hash(password)
            self.created_at = datetime.now()

    def set_id(self, id_):
        self.id = id_

    def get_values(self):
        return self.email, self.password, self.created_at

    def save(self):
        db.insert_one(table=self.table, obj=self)

    def __str__(self):
        return '{0}, {1}, {2}'.format(self.id, self.email, self.password, self.created_at)

    @classmethod
    def login(cls, email, password):
        obj = cls.get_objs(email=email)
        if obj:
            return check_password_hash(obj.password, password)
        else:
            return False

    @classmethod
    def register(cls, email, password):
        obj = cls(email, password)
        obj.save()
        return obj
