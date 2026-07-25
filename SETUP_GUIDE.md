# Scottish Football Database - Django Setup Guide

## Prerequisites
- Python 3.9+
- PostgreSQL running with `scottish_football` database created
- User `mundar` with superuser privileges

## Installation Steps

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Create Django Project
```bash
django-admin startproject config .
django-admin startapp football
```

### 4. Copy Configuration Files
- Copy the contents of `settings.py` snippet into `config/settings.py`
- Copy `models.py` into `football/models.py`
- Copy `admin.py` into `football/admin.py`
- Copy `serializers.py` and `views.py` into `football/`
- Copy `urls.py` into `football/urls.py`
- Update `config/urls.py` to include the football app URLs

### 5. Create Database Tables
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser for Admin
```bash
python manage.py createsuperuser
```

### 7. Run Development Server
```bash
python manage.py runserver
```

Access:
- **Admin Panel:** http://localhost:8000/admin
- **API:** http://localhost:8000/api/

## Project Structure
```
.
├── config/
│   ├── settings.py          (update with provided snippet)
│   ├── urls.py              (add football URLs)
│   └── ...
├── football/
│   ├── models.py            (Django models)
│   ├── admin.py             (Admin config)
│   ├── serializers.py       (DRF serializers)
│   ├── views.py             (API views)
│   ├── urls.py              (URL routing)
│   └── ...
├── venv/
├── manage.py
└── requirements.txt
```

## Available API Endpoints

### Matches
- `GET /api/matches/` - List all matches
- `GET /api/matches/<id>/` - Match detail
- `POST /api/matches/` - Create match

### Players
- `GET /api/players/` - List all players
- `GET /api/players/<id>/` - Player detail
- `POST /api/players/` - Create player

### Teams
- `GET /api/teams/` - List all teams
- `GET /api/teams/<id>/` - Team detail
- `POST /api/teams/` - Create team

### Competitions
- `GET /api/competitions/` - List competitions
- `GET /api/competitions/<id>/` - Competition detail

### Query Examples
```
# Find matches by team
GET /api/matches/?home_team=1

# Find player by name
GET /api/players/?last_name=Law

# Find matches in date range
GET /api/matches/?match_date__gte=1950-01-01&match_date__lte=1960-12-31
```

## Admin Panel Features
- Add/edit/delete matches, players, teams
- Bulk actions (delete multiple records)
- Search by name, date, etc.
- Filtering by competition, season, venue

## Next Steps
1. Load historical data via admin panel or CSV import
2. Build React frontend to consume the API
3. Add authentication for data editors
4. Deploy to production (Heroku/Digital Ocean)
