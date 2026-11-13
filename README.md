# Job Application Tracker API

A REST API for tracking job applications, built with Django and Django REST Framework. Each user has a private account and sees only their own applications.

## Features
- User registration (with password validation) and token login
- Add, edit, delete, and list job applications
- Statuses: applied, interview, offer, rejected
- Filter by status: `?status=interview`
- Summary endpoint with counts per status
- Privacy: users can never see or edit each other's data

## Tech
Python, Django, Django REST Framework, SQLite

## Run it locally
```bash
git clone https://github.com/sumi74/Job-tracker-api.git
cd Job-tracker-api
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
python -m pip install django djangorestframework
python manage.py migrate
python manage.py runserver
```

## Run the tests
```bash
python manage.py test
```

## Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/register/` | Create an account |
| POST | `/api/login/` | Get an auth token |
| GET/POST | `/api/applications/` | List / add applications |
| GET/PUT/PATCH/DELETE | `/api/applications/{id}/` | Manage one application |
| GET | `/api/applications/summary/` | Counts per status |

## Example
```json
POST /api/applications/
{"company": "Acme Ltd", "role": "Junior Backend Developer", "status": "applied"}
```


## Live demo
https://job-application-tracker-api-4jto.onrender.com/api/

Hosted on Render's free tier, so the first request after a quiet period can take about a minute while the server wakes up. Data on the free tier may reset, so treat it as a demo.

Try it:
1. Create an account at `/api/register/`
2. Log in at `/api-auth/login/`
3. Add and view applications at `/api/applications/`