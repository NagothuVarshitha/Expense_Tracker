# ExpenseTracker

## Project Overview
ExpenseTracker is a beginner-friendly personal finance tracker built with Django. Users can securely register, record income and expenses, review their balance, and explore spending by category.

## Features
- Session-based registration, login, logout, and Django password hashing
- User-owned transaction CRUD with server-side validation
- Dashboard totals for income, expenses, balance, and savings
- Search and filters for title, type, category, and date
- Responsive Django templates with a Chart.js expense breakdown
- REST API using Django REST Framework
- Django Admin management and a demo data command

## Tech Stack
Python 3, Django 5.2, Django REST Framework, MySQL, HTML5, CSS3, Bootstrap 5, Chart.js.

## Project Structure
`config/` contains settings and project routing. `finance/` contains the model, forms, views, serializers, API, admin, tests, and demo command. `templates/` contains the Django UI and `static/` contains CSS and JavaScript.

## Prerequisites
Install Python 3.11+ and MySQL 8+. The app uses SQLite automatically when `DB_NAME` is not configured, so the first local run does not require MySQL.

## MySQL Setup
Open MySQL Workbench or the MySQL shell and run:

```sql
CREATE DATABASE expensetracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Copy `.env.example` to `.env` and set `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, and `DB_PORT`. When `DB_NAME` is present, Django uses MySQL. Leave those variables out for the zero-setup SQLite mode.

## Installation on Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/ in a browser. Register a new account, or create demo data with:

```powershell
python manage.py seed_demo
```

Demo login: `demo` / `DemoPass123!`.

## API Endpoints
All API endpoints require an authenticated Django session and are scoped to the logged-in user.

- `GET /api/transactions/`
- `POST /api/transactions/`
- `GET /api/transactions/<id>/`
- `PUT /api/transactions/<id>/`
- `PATCH /api/transactions/<id>/`
- `DELETE /api/transactions/<id>/`
- `GET /api/dashboard/`

For browser testing, sign in first and visit an API URL. For a JSON POST, send fields `title`, `amount`, `transaction_type`, `category`, `description`, and `date`; the server assigns the user from the session.

## Testing

```powershell
python manage.py check
python manage.py test
```

The test suite covers registration, login, CRUD, dashboard totals, authentication, API behavior, and user isolation.
