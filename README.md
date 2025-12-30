# SecureMS – Secure Microservice-Based Web Application

## Requirements
- Python 3.10+
- pip
- virtualenv

## Setup Instructions

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
