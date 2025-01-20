from yandex_business_ai_landing.model import User
from yandex_business_ai_landing.app import db

def test_user_creation(init_database):
    user = User(username="user", password="password")
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == "user"


def test_user_query(init_database):
    user = User(username="test_user_query", password="password")
    db.session.add(user)
    db.session.commit()

    retrieved_user = User.query.filter_by(username="test_user_query").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "test_user_query"
