# AI Бизнес помощник Landing

prod https://business.t3t.online
test https://business-test.t3t.online

### Supported Platforms

### Ubuntu

Follow the instructions below to set up the project on Ubuntu:

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```
This project supports both macOS and Windows. Below are the setup instructions for each platform.

### macOS

Follow the instructions below to set up the project on macOS:

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

### Windows

Follow the instructions below to set up the project on Windows:

Create a virtual environment:
```bash
python -m venv venv
```

Activate the virtual environment:
```bash
venv\Scripts\activate
```
This project is a landing page for AI Бизнес помощник, built using Flask. It includes user authentication with login and registration functionality.

## Project Setup

### Prerequisites
* Python 3.x
* Virtual environment (venv)

### Installation

Clone the repository:
```bash
git clone <repository-url>
cd yandex_business_ai_landing
```

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
```bash
source venv/bin/activate
```

Install the required packages:
```bash
pip install Flask Flask-SQLAlchemy Flask-Login
```

## Database Setup
Delete the existing database file (if it exists):
```bash
rm ./instance/users.db
```

Create the database and tables:
```bash
python create_db.py
```

Mark migrations as completed without running them
```
flask db stamp head
```

Apply the migrations to the database:
```
flask db upgrade   
```

## Running the Application

Run the Flask application:
```bash
flask run
```

## Build docker image
### In the directory yandex_business_ai_landing

docker build -t business-ai .

## Running application in Docker container

docker run -p 5000:5000 -v business-ai/app/instance:/{path to yandex_business_ai_landing}/instance business-ai


Access the application: Open your web browser and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).

## Project Structure

```
yandex_business_ai_landing/
├── app.py
├── create_db.py
├── templates/
│   ├── index.html
│   ├── login.html
│   └── register.html
├── static/
├── venv/
└── README.md
```

## Routes

* `/`: Home page with links to login and registration.
* `/login`: Login page.
* `/register`: Registration page.
* `/personal_cabinet`: Personal cabinet page (requires authentication).
```
