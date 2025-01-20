# Testing Flask Applications

## File Structure

A common file structure for a Flask application with tests might look like this:

```
/my_flask_app/
│
├── /app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── utils.py
│
├── /tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_utils.py
│
├── /static/
│   └── ...
│
├── /templates/
│   └── ...
│
├── config.py
├── requirements.txt
└── run.py
```

## Organizing Tests

### Setup and Configuration

- Use a `conftest.py` file in the `tests/` directory to define fixtures and configuration for your tests.
- Create a `config_test.py` file to specify test-specific configurations.

### Test Files

- Each module or component of your application should have its corresponding test file (e.g., `test_models.py`, `test_routes.py`).
- Use descriptive names for test functions and classes to make it clear what is being tested.

### Fixtures

- Use fixtures to set up the environment before each test, such as initializing a test database or creating mock objects.
- Fixtures can be defined in `conftest.py` or within individual test files.

### Mocking and Patching

- Use mocking libraries like `unittest.mock` to isolate tests from external dependencies (e.g., databases, APIs).

### Test Cases

- Write test cases for different scenarios, including edge cases.
- Ensure that each test is independent and does not rely on the state of other tests.

## Example Test Setup

### `conftest.py`

```python
import pytest
from app import create_app, db
from config_test import Config


@pytest.fixture(scope='module')
def test_client():
    app = create_app(Config)
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client


@pytest.fixture(scope='module')
def init_database(test_client):
    # Create the database and the database table
    db.create_all()

    # Insert data into the database
    # Example: user = User(username="testuser")
    # db.session.add(user)
    # db.session.commit()

    yield  # This is where the testing happens!

    # Teardown : clean up after tests are done
    db.drop_all()
```

### `config_test.py`

```python
import os

class Config:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SECRET_KEY = 'test_secret_key'
    WTF_CSRF_ENABLED = False
```

### `tests/test_routes.py`

```python
def test_index(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"Главная страница AI Бизнес помощник" in response.data


def test_login_page(test_client):
    response = test_client.get('/login')
    assert response.status_code == 200
    assert b"Войти" in response.data
```

## Tracking Test Coverage

### Install `coverage.py`

```bash
pip install coverage
```

### Run Tests with Coverage

```bash
coverage run -m pytest
```

### Generate a Report

```bash
coverage report -m
```

### HTML Report

```bash
coverage html
```
This will generate an `htmlcov/` directory with an HTML report that you can open in your browser.

### Example Coverage Command

```bash
coverage run -m pytest && coverage report -m && coverage html
```

This command will:
- Run all tests and collect coverage data.
- Print a text-based coverage report to the console.
- Generate an HTML coverage report in the `htmlcov/` directory.