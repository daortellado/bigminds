from datetime import datetime

from app import database

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.dialects.mysql import TIME

class Instance(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    chat_enabled = database.Column(database.Boolean, nullable=False, default=True)
    homepage_title = database.Column(database.String(200), default='Chat Application')
    homepage_hex_color = database.Column(database.String(6), default='ffd0cc')
    media_file = database.Column(database.String(200), nullable=False, default='default.jpg')
    media_file_is_default = database.Column(database.Boolean, nullable=False, default=True)
    media_is_video = database.Column(database.Boolean, nullable=False, default=False)
    page_views = database.Column(database.Integer, nullable=False, default=0)

class Message(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_posted = database.Column(database.String(30))
    name = database.Column(database.String(100), default='')
    content = database.Column(database.String(500), default='')

class EduSchedu(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    time = database.Column(TIME(), nullable=False)
    dow = database.Column(database.Integer, default='')
    classname = database.Column(database.String(100), default='')
    zoomlink = database.Column(database.String(500), default='')

class ClassNotiQueue(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    linkcont = database.Column(database.String(500))
    now = database.Column(database.String(30))
    nameclass = database.Column(database.String(30))

# class UserLogin(UserMixin):

#     # def __init__(self, id):
#     #     self.id = id
#     #     self.name = "user" + str(id)
#     #     self.password = self.name + "_secret"
        
#     def __repr__(self):
#         return "%d/%s/%s" % (self.id, self.name, self.password)

# users = [UserLogin(id) for id in range(1, 21)]

class User(UserMixin, database.Model):
    """User account model."""
    __tablename__ = 'flasklogin-users'
    id = database.Column(database.Integer,
                   primary_key=True)
    name = database.Column(database.String(100),
                     nullable=False,
                     unique=False)
    email = database.Column(database.String(40),
                      unique=True,
                      nullable=False)
    role = database.Column(database.String(40),
                      unique=True,
                      nullable=False)
    password = database.Column(database.String(200),
                         primary_key=False,
                         unique=False,
                         nullable=False)
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return self.password
        # return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

database.create_all()
database.session.commit()

# Creating an "Instance" model if there is none.
if Instance.query.get(1) is None:
    database.session.add(Instance())
    database.session.commit()