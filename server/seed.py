#!/usr/bin/env python3

# Standard library imports
from random import randint

# Remote library imports
from faker import Faker
from flask_bcrypt import Bcrypt
import datetime

# Local imports
from app import app
from models import db, Sensor, DataPoint, Status, User

faker = Faker()

# Manufacturer and model information
manu_model_list = [
    {'Dexcom': ['G7', 'G6 Personal', 'G6 Pro']}, 
    {'Medtronic': ['Guardian Sensor 3']}, 
    {'Abbott': ['FreeStyle Libre 2', 'FreeStyle Libre 3']}, 
    {'Eversense': ['E3']}, 
    {'Roche': ['Accu-Chek SmartGuide']}
    ]

# Base Users
users_list = [
    {'first_name': 'Jeanette',
     'last_name': 'Burr',
     'manufacturer': 'Dexcom',
     'model': 'G6 Pro',
     'gender': 'F',
     'birthday': datetime.date(2001, 9, 3),
     'date_joined': datetime.date(2016, 10, 2),
    },
    {'first_name': 'Tracy',
     'last_name': 'Axel',
     'manufacturer': 'Abbott',
     'model': 'FreeStyle Libre 3',
     'gender': 'F',
     'birthday': datetime.date(1999, 2, 3),
     'date_joined': datetime.date(2016, 3, 17),
    },
    {'first_name': 'Chance',
     'last_name': 'Nickels',
     'manufacturer': 'Medtronic',
     'model': 'Guardian Sensor 3',
     'gender': 'M',
     'birthday': datetime.date(2003, 10, 8),
     'date_joined': datetime.date(2015, 1, 1),
    },
    {'first_name': 'Justin',
     'last_name': 'Bacon',
     'manufacturer': 'Eversense',
     'model': 'E3',
     'gender': 'M',
     'birthday': datetime.date(1973, 9, 10),
     'date_joined': datetime.date(2017, 4, 19),
    },
    {'first_name': 'Patrick',
     'last_name': 'Charles',
     'manufacturer': 'Dexcom',
     'model': 'G7',
     'gender': 'M',
     'birthday': datetime.date(1983, 3, 1),
     'date_joined': datetime.date(2016, 6, 30),
    }
]

# Seeding for sensors
def create_sensors():
    sensors = []
    for _ in range(15):
        num = randint(0,4)
        date_list = generate_app_rem_dates()
        s = Sensor(
            manufacturer = users_list[num]['manufacturer'],
            model = users_list[num]['model'],
            application_date = date_list[0],
            removal_date = date_list[1],
            serial = faker.bothify(text='??#####?#?'),
            user_id = num + 1
        )
        sensors.append(s)
    for _ in range (5):
        date_list = generate_app_rem_dates()
        s = Sensor(
            manufacturer = "Dexcom",
            model = "G6 Pro",
            application_date = date_list[0],
            removal_date = date_list[1],
            serial = faker.bothify(text='??#??##?#?'),
            user_id = 6
        )
        sensors.append(s)
    return sensors

def generate_app_rem_dates():
    app = fake.date_between(start_date='-5y', end_date='now')
    rem = app + datetime.timedelta(days=14)
    return [app, rem]

# Seeding for users
def create_users():
    users = []
    for user in users_list:
        password = fake.word() + str(randint(0,99)) + fake.word()
        u = User(
            username = fake.word() + fake.word() + str(randint(0,99)),
            _password_hash = bcrypt.generate_password_hash(password),
            date_joined = user['date_joined'],
            first_name = user['first_name'],
            last_name = user['last_name'],
            birthday = user['birthday'],
            age = randint(21, 99),
            gender = user['gender'],
            email = fake.email()
        )
        users.append(u)
    return users

# Seeding for statuses
def create_statuses():
    statuses = []
    status_list = [
        {'severity': 'Low',
         'min': 30,
         'max': 49
        },
        {'severity': 'Excellent',
         'min': 50,
         'max': 115
        },
        {'severity': 'Good',
         'min': 116,
         'max': 180
        },
        {'severity': 'Elevated',
         'min': 181,
         'max': 214
        },
        {'severity': 'Action Suggested',
         'min': 215,
         'max': 380
        }
    ]
    for status in status_list:
        s = Status(
            severity = status['severity'],
            min = status['min'],
            max = status['max']
        )
        statuses.append(s)
    return statuses

# Seeding for datapoints
def create_datapoints():
    datapoints = []
    for sensor in Sensor.query.all():
        date = sensor.application_date
        for _ in range(14):
            bgl_num = randint(35, 214)
            d = DataPoint(
                date_time = date,
                bgl = bgl_num,
                sensor_id = sensor.id,
                status_id = assign_status_id(bgl_num)
            )
            date = date + datetime.timedelta(days=1)
            datapoints.append(d)
    return datapoints

def assign_status_id(bgl):
    for status in Status.query.all():
        if status.min <= bgl <= status.max:
            return status.id
    return None

if __name__ == '__main__':
    fake = Faker()
    bcrypt = Bcrypt()
    with app.app_context():
        print("Starting seed...")
        print("Clearing db...")
        Sensor.query.delete()
        DataPoint.query.delete()
        Status.query.delete()
        User.query.delete()

        print("Seeding sensors...")
        sensors = create_sensors()
        db.session.add_all(sensors)
        db.session.commit()

        print("Seeding statuses...")
        statuses = create_statuses()
        db.session.add_all(statuses)
        db.session.commit()

        print("Seeding users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding datapoints...")
        datapoints = create_datapoints()
        db.session.add_all(datapoints)
        db.session.commit()

        print("Done seeding!")
