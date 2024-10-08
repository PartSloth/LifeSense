from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class Sensor(db.Model, SerializerMixin):
    __tablename__ = 'sensors'

    id = db.Column(db.Integer, primary_key = True)
    manufacturer = db.Column(db.String)
    model = db.Column(db.String)
    application_date = db.Column(db.DateTime)
    removal_date = db.Column(db.DateTime)
    serial = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', back_populates='sensors')
    datapoints = db.relationship('DataPoint', back_populates='sensor', cascade='all, delete-orphan')

    serialize_rules = ('-user.sensors', '-datapoints.sensor')

class DataPoint(db.Model, SerializerMixin):
    __tablename__ = 'datapoints'

    id = db.Column(db.Integer, primary_key = True)
    date_time = db.Column(db.DateTime)
    bgl = db.Column(db.Integer)
    sensor_id = db.Column(db.Integer, db.ForeignKey('sensors.id'))
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.id'))

    sensor = db.relationship('Sensor', back_populates='datapoints')
    status = db.relationship('Status', back_populates='datapoints')

    serialize_rules = ('-sensor.datapoints', '-status.datapoints')

class Status(db.Model, SerializerMixin):
    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key = True)
    severity = db.Column(db.String)
    min = db.Column(db.Integer)
    max = db.Column(db.Integer)

    datapoints = db.relationship('DataPoint', back_populates='status', cascade='all, delete-orphan')

    serialize_rules = ('-datapoints.status', )

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String)
    _password_hash = db.Column(db.String)
    date_joined = db.Column(db.DateTime)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    birthday = db.Column(db.String)
    age = db.Column(db.Integer)
    gender = db.Column(db.String)

    sensors = db.relationship('Sensor', back_populates='user', cascade='all, delete-orphan')

    serialize_rules = ('-sensors.user', )

    @hybrid_property
    def password_hash(self):
        raise Exception('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password)