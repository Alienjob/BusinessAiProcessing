import pytest
from yandex_business_ai_landing.app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client

@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert data into the database if needed
    from yandex_business_ai_landing.model.user import User
    user = User(username="testuser", password="testpassword")
    db.session.add(user)
    db.session.commit()

    yield  # This is where the testing happens!

    # Teardown : clean up after tests are done
    db.drop_all()