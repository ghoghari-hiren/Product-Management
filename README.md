# Project Setup Instructions

## 1. Clone the Repository
```bash
git clone <repository_url>
cd <project_directory>
```

## 2. Create Virtual Environment
```bash
python -m venv venv
# Activate on Windows
venv\Scripts\activate
# Activate on macOS/Linux
source venv/bin/activate
```

## 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

## 5. Create Superuser / Admin
```bash
python manage.py createsuperuser
```
Follow the prompts to create admin credentials.

## 6. Run Development Server
```bash
python manage.py runserver
```
Access the application at `http://127.0.0.1:8000/`


## 7. Notes
- JWT access tokens are configured to expire in 2 hours.
- Rate limiting is applied to all endpoints.
- Product logs are tracked using Django signals.
- delete is implemented; products are disabled by setting `is_active=False`.
