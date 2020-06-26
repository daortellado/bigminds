from datetime import datetime

from app import database

from flask_login import UserMixin

from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy.dialects.mysql import TIME

from hashlib import md5

student_identifier = database.Table('student_identifier',
    database.Column('class_id', database.Integer, database.ForeignKey('classes.id')),
    database.Column('user_id', database.Integer, database.ForeignKey('flasklogin-users.id'))
)
student_appt = database.Table('student_appt',
    database.Column('appt_id', database.Integer, database.ForeignKey('appts.id')),
    database.Column('user_id', database.Integer, database.ForeignKey('flasklogin-users.id'))
)

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

class Channel(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    date_posted = database.Column(database.String(30))
    name = database.Column(database.String(100), default='')
    content = database.Column(database.String(500), default='')

class EduSchedu(database.Model):
    __tablename__ = 'classes'
    id = database.Column(database.Integer, primary_key=True)
    time = database.Column(TIME(), nullable=False)
    dow = database.Column(database.Integer, default='')
    classname = database.Column(database.String(100), default='')
    zoomlink = database.Column(database.String(500), default='')
    students = database.relationship("User",
                               secondary=student_identifier, backref=database.backref('students'), lazy = 'dynamic')

class ApptSchedu(database.Model):
    __tablename__ = 'appts'
    id = database.Column(database.Integer, primary_key=True)
    time = database.Column(TIME(), nullable=False)
    dow = database.Column(database.Integer, default='')
    teacher = database.Column(database.String(100), default='')
    zoomlink = database.Column(database.String(500), default='')
    apptstudents = database.relationship("User",
                               secondary=student_appt, backref=database.backref('apptstudents'), lazy = 'dynamic')

class ClassNotiQueue(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    linkcont = database.Column(database.String(500))
    now = database.Column(database.String(30))
    nameclass = database.Column(database.String(30))

class ApptNotiQueue(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    linkcont = database.Column(database.String(500))
    now = database.Column(database.String(30))
    teacher = database.Column(database.String(30))

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
    enrolled = database.relationship("EduSchedu",
                               secondary=student_identifier, backref=database.backref('enrolled'), lazy = 'dynamic')
    approlled = database.relationship("ApptSchedu",
                               secondary=student_appt, backref=database.backref('approlled'), lazy = 'dynamic')
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)
    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return self.password
    def __repr__(self):
        return "%s" % (self.name)
        # return check_password_hash(self.password, password)

    # def __repr__(self):
    #     return '<User {}>'.format(self.name)


database.create_all()
database.session.commit()

# Creating an "Instance" model if there is none.
if Instance.query.get(1) is None:
    database.session.add(Instance())
    database.session.commit()