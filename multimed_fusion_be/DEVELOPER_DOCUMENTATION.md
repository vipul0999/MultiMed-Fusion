# Developer Documentation

## Wiki URL

Add your project wiki URL here before submission:

`<PASTE_WIKI_URL_HERE>`

## Project Overview
    
    Github Repo: https://github.com/vipul0999/MultiMed-Fusion

## Tools and Services Used

### Backend

- Python 3.11 recommended by the project README
- Django
- Django REST Framework
- Simple JWT (`djangorestframework-simplejwt`)
- PostgreSQL
- `python-dotenv` for loading environment variables from `.env`
- `drf-yasg` for Swagger/OpenAPI docs
- `django-cors-headers`
- Pillow
- `python-magic`
- `gunicorn`
- OpenAI SDK
- Google GenAI SDK
- `ruff`, `black`, and `pre-commit` for code quality

### Frontend

- Node.js
- npm
- React
- Vite
- Axios
- React Router
- Framer Motion
- ESLint

### External Services

- PostgreSQL database
- SMTP email via Gmail in the current backend `.env`
- LLM provider support:
  - Google Gemini
  - OpenAI

Each developer should create their own local `.env` values.

## Development Environment Setup

### Recommended Environment

Use WSL Ubuntu for both projects. The frontend build tools do not behave reliably when launched from a Windows UNC path such as `\\wsl.localhost\...`.

## Backend Setup

### 1. Create and activate a virtual environment

From WSL:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install backend dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a local `.env`

There is an `.env.sample` file in the backend root. Copy it and fill in your own values:

```bash
cp .env.sample .env
```

Suggested local development values:

```env
DEBUG=1
DJANGO_SETTINGS_MODULE=backend.settings
SECRET_KEY=replace_with_your_own_secret_key
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_DB=ctf_db
POSTGRES_USER=django_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_app_password
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=models/gemini-2.5-flash-lite
```

Notes:

- `manage.py` loads `.env` automatically using `python-dotenv`.
- `STATIC_ROOT` and `MEDIA_ROOT` are optional for local development because the settings file falls back to local project folders.
- The checked-in `.env` contains real-looking secrets. A new developer should not reuse them. Replace all secrets with personal/local credentials.

### 4. Set up PostgreSQL

Create a PostgreSQL database and matching user credentials for the values in `.env`.

Example:

- Database: `db`
- User: `django_user`
- Password: choose your own password
- Host: `127.0.0.1`
- Port: `5432`

If a developer wants to use their own PostgreSQL account, they only need to change:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

No source code changes are required for that switch because Django reads these from environment variables.

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Optional: seed demo data

The backend contains a management command that creates demo users, groups, contests, challenges, blogs, chat history, and submissions:

```bash
python manage.py seed_demo
```


### 7. Start the backend server

```bash
python manage.py runserver
```

Backend URLs:

- App/API base: `http://127.0.0.1:8000/`


## Frontend Setup



### 1. Use WSL and install dependencies there

```bash
npm install
```

### 2. Configure the frontend `.env`

Current file:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

If a developer points the frontend to another backend, they only need to change `VITE_API_BASE_URL`.

### 3. Start the frontend dev server

```bash
npm run dev
```

### 4. Production build

```bash
npm run build
```

## Directions to Run the Code for Testing

## Backend Testing

The backend test suite was verified with:

```bash
source venv/bin/activate
python manage.py test --settings=backend.test_settings
```


## Frontend Testing / Validation

There is currently no `test` script in `package.json`.

Available frontend commands are:

- `npm run dev`
- `npm run build`
- `npm run lint`
- `npm run preview`

Recommended validation flow:

1. Run `npm install`
2. Run `npm run dev`
3. Open the local Vite URL shown in the terminal
4. Verify login, registration, and routed pages load

## How to Use Personal Service Accounts

### PostgreSQL

Developers can use their own local PostgreSQL instance by changing only the backend `.env` database values:

- `POSTGRES_DB`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_HOST`
- `POSTGRES_PORT`

### Email Service

The backend is configured for Gmail SMTP:

- `EMAIL_HOST_USER`
- `EMAIL_HOST_PASSWORD`


### LLM Provider

The backend supports either Gemini or OpenAI through environment variables.

To use Gemini:

```env
LLM_PROVIDER=gemini
GEMINI_API_KEY=your_key
GEMINI_MODEL=models/gemini-2.5-flash-lite
```

To use OpenAI:

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini
```

No code changes are required to switch providers if the correct environment variables are supplied.

## Known Developer Notes

- The backend hardcodes `DEBUG = True` and `ALLOWED_HOSTS = ['*']` in `backend/settings.py`, even though `.env` contains related variables. This is acceptable for local development but should be cleaned up for production.
- The frontend currently expects endpoints beginning with `/api/...`.

## Quick Start Summary

### Backend

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.sample .env
python manage.py migrate
python manage.py test --settings=backend.test_settings
python manage.py runserver
```

### Frontend

```bash
cd "/home/anil/gdp 2/gdp_fe"
npm install
npm run dev
```
