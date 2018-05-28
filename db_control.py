from app import db,app
from app.models import UserInfo


def create_database():
    db.create_all()

def query_dataset():
    return UserInfo.query.all()

def add_record(user):
    db.session.add(user)
    db.session.commit()


if __name__ == '__main__':
    create_database()
