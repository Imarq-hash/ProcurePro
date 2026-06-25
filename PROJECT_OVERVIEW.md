# ProcurePro Project Overview

## Tech Stack

- Python 3
- Django 6.0.4
- SQLite (default Django database)
- HTML + CSS + JavaScript for frontend templates
- Django template engine with `{% load static %}` and static asset management
- Django ORM for database models
- `django.contrib.admin`, `django.contrib.auth`, `django.contrib.sessions`, `django.contrib.messages`, `django.contrib.staticfiles`
- `django-ratelimit` for request throttling
- `python-dotenv` for environment configuration via `.env`

## Project Structure

- `manage.py` - Django management entrypoint
- `procurepro_project/` - Django project config
  - `settings.py` - application settings, static/media paths, auth model, security config
  - `urls.py` - root URL routes
  - `wsgi.py` / `asgi.py` - WSGI/ASGI app entrypoints
- `procurement/` - main app
  - `models.py` - custom `User`, `ContractorProfile`, `AdminProfile`, `Tender`, `Bid`, `Notification`, `TenderRequest`, etc.
  - `views.py` - app views and page handlers
  - `urls.py` - application routes
  - `tests.py` - test cases
  - `migrations/` - database migration history
- `templates/` - HTML template files for pages and admin views
- `static/` - static assets
  - `css/styles.css`
  - `js/script.js`
  - `assets/` - image assets used by pages
- `media/` - uploaded files during runtime

## Key Features

- Custom email-based authentication with `AUTH_USER_MODEL = 'procurement.User'`
- Contractor and admin roles via `User.Role`
- Tender listing, bidding, and user dashboards
- Admin portal for tender management and review
- Notifications and request submission flows
- File upload validation for documents
- Rate limiting on sign-in and request submission endpoints

## Static Asset Configuration

- `STATIC_URL = '/static/'`
- `STATICFILES_DIRS = [BASE_DIR / 'static']`
- `STATIC_ROOT = BASE_DIR / 'staticfiles'`
- Development static serving added in `procurepro_project/urls.py`
- Current CSS count: `1` file (`static/css/styles.css`)

## Routing Summary

- Root pages: `/`, `/signin/`, `/signup/`, `/tenders/`, `/contractors/`, `/help-center/`
- Auth/actions: `/logout/`, `/request-tender/`
- Dashboard pages: `/dashboard/`, `/my-bids/`, `/settings/`
- Admin pages: `/admin-login/`, `/admin-dashboard/`, `/admin-post-tender/`, `/admin-manage-tenders/`, `/admin-tender-requests/`, `/admin-contractors/`, `/admin-review-bids/`, `/admin-reports/`
- Notification endpoints: `/notifications/mark-read/<pk>/`, `/notifications/mark-all-read/`

## Important Notes

- The project uses a `.env` file for configuration. Local development should use `DEBUG=True` to serve static files automatically.
- The app currently has a single CSS file, so all pages depend on `static/css/styles.css` for styling.
- Static files are served from the `static/` directory during development.

## Running Locally

1. Activate the virtual environment if one exists.
2. Ensure `.env` is configured.
3. Run `python manage.py runserver 3000`
4. Visit `http://127.0.0.1:3000/`

## Current Fixes Applied

- Added explicit development static routing in `procurepro_project/urls.py`
- Set `DEBUG=True` in `.env` for local development testing

## How it works

- **Signup & Authentication**: Users register via the `/signup/` page. The app uses a custom `User` model with `email` as the username. Passwords are validated using Django validators plus a custom complexity validator. On successful signup the user is logged in and redirected to `/dashboard/`.

- **Tender Discovery & Details**: Public pages like `/tenders/` and `/tenders/<id>/details/` list open tenders. Each tender stores metadata (title, description, category, deadlines, budget ranges) in the `Tender` model.

- **Submit Tender Requests & Bids**: Authenticated contractors submit tender requests via `/request-tender/`. Contractors submit bids on tender detail pages (`/tenders/<id>/submit/`). Bids are stored in the `Bid` model and include amount, duration, and proposal text.

- **Admin Review & Publishing**: Admin users access `/admin-dashboard/` and related admin routes to post, review, and publish tenders. Admin actions generate `Notification` entries for affected users.

- **Notifications & Dashboard**: Notifications are stored in the `Notification` model and surfaced in the header dropdown and dashboard. Users can mark notifications read via `/notifications/mark-read/<pk>/` and `/notifications/mark-all-read/`.

- **File uploads & Validation**: Uploaded documents are saved under `media/` with validation for file size, extension, and content type enforced in the views and model validators.

- **Static files & Assets**: Static files are kept in `static/` and served from `/static/`. For local development `STATIC_URL`, `STATICFILES_DIRS`, and the added static route in `procurepro_project/urls.py` allow direct serving of CSS, JS, and images. In production, static files should be collected to `STATIC_ROOT` and served by the web server or a CDN.
