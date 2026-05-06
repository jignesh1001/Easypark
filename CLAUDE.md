# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
EasyPark is a Django-based parking application that allows users to find, reserve, and manage parking spaces. The application features:
- User authentication (login/signup)
- User type selection (owner/customer)
- Parking space listing and management
- Booking system for parking spots
- Real-time availability tracking

## Setup and Development

### Initial Setup
1. Clone the repository
2. Create and activate a virtual environment:
   - Windows: `python -m venv venv` then `venv\Scripts\activate`
   - Unix/MacOS: `python -m venv venv` then `source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt` (if exists)
   - Note: If no requirements.txt exists, install Django: `pip install django`
4. Apply database migrations: `python manage.py migrate`
5. Create a superuser (optional): `python manage.py createsuperuser`
6. Run the development server: `python manage.py runserver`

### Common Commands
- Start development server: `python manage.py runserver`
- Run migrations: `python manage.py migrate`
- Create new migrations: `python manage.py makemigrations`
- Create superuser: `python manage.py createsuperuser`
- Collect static files: `python manage.py collectstatic`
- Run tests: `python manage.py test`

## Project Structure
```
├── manage.py              # Django management script
├── db.sqlite3             # SQLite database (development)
├── requirements.txt       # Python dependencies (if present)
├── parkproject/           # Django project settings
│   ├── __init__.py
│   ├── settings.py        # Django settings
│   ├── urls.py            # URL routing
│   ├── wsgi.py            # WSGI configuration
│   └── asgi.py            # ASGI configuration
├── parkapp/               # Main application
│   ├── migrations/        # Database migrations
│   ├── __init__.py
│   ├── admin.py           # Admin interface configuration
│   ├── apps.py            # App configuration
│   ├── models.py          # Data models
│   ├── views.py           # View logic
│   ├── urls.py            # App-specific URL routing
│   ├── forms.py           # Form definitions
│   └── tests.py           # Tests
├── static/                # Static files (CSS, JS, Images)
└── templates/             # HTML templates
```

## Key Components

### Models (parkapp/models.py)
- **TYPER**: User type (owner/customer) linked to user
- **OWNER**: Parking space owners with location, capacity, pricing
- **CUSTOMER**: Customer profile linked to Django User
- **BOOK**: Booking records linking customers to parking spots

### Views (parkapp/views.py)
- **index**: Landing page (redirects authenticated users to main)
- **login/logout**: Authentication views
- **signup**: User registration
- **main**: Dashboard showing available parking spots and user bookings
- **usertype**: Select user type (owner/customer)
- **addinfo**: Add parking space (for owners)
- **book_spot**: Book a parking spot
- **accept/decline/free_slot**: Manage booking status

### URLs (parkapp/urls.py)
- Root (`/`): Index page
- `/login`, `/signup`, `/main`: Authentication and dashboard
- `/usertype`, `/addinfo`, `/create_profile`: User setup
- `/book_spot/<id>`: Book a specific spot
- `/accept/<id>`, `/decline/<id>`, `/free_slot/<id>`: Booking management

### Templates
Located in the `templates/` directory, HTML files correspond to each view:
- `index.html`: Landing page
- `login.html`, `signup.html`: Authentication forms
- `main.html`: Dashboard with parking listings
- `book.html`: Booking form
- And others for various pages

## Database
- Uses SQLite3 by default (development)
- Database file: `db.sqlite3` in project root
- To reset database: Delete `db.sqlite3` and run `python manage.py migrate`

## Static and Media Files
- Static files (CSS, JS): Served from `/static/` directory
- Media files (uploads): Served from `/images/` directory
- Configured in settings.py with `STATIC_URL`, `MEDIA_URL`, and `STATICFILES_DIRS`

## Development Guidelines
1. Always activate the virtual environment before working
2. Run migrations after model changes
3. Keep DEBUG=True in settings.py for development (change for production)
4. Follow Django conventions for naming and structure
5. Test changes thoroughly before committing

## Notes
- The application uses function-based views
- Forms are defined in forms.py for validation
- Bootstrap-like styling may be present in templates
- No external APIs or services are currently integrated