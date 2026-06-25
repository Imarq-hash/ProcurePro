# ProcurePro — Local Development README

This README explains how to set up and run the ProcurePro Django project locally, and includes troubleshooting steps for common issues (especially static file serving).

## Prerequisites

- Python 3.10+ (use the project's virtual environment if available)
- pip
- (Optional) Git

## Quick Start (Windows)

1. Open PowerShell and change to the project directory:

```powershell
cd "C:\Users\Irene\Desktop\PROJECT\Codes sys"
```

2. (Optional) Activate virtual environment if present:

```powershell
# If the project uses a virtualenv in .venv
. .venv\Scripts\Activate.ps1
# or with cmd.exe
.venv\Scripts\activate.bat
```

3. Install dependencies (if a requirements file exists):

```powershell
pip install -r requirements.txt
```

4. Ensure environment variables are set. The project uses a `.env` file in the repo root. Example values (do NOT use these in production):

```
SECRET_KEY=your-insecure-secret-key-change-this-in-production-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run database migrations (first time):

```powershell
python manage.py migrate
```

6. Create a superuser (optional):

```powershell
python manage.py createsuperuser
```

7. Start the development server on port 3000:

```powershell
python manage.py runserver 3000
```

8. In a second terminal, start the livereload watcher server:

```powershell
python manage.py livereload
```

9. Open the app in a browser:

```
http://127.0.0.1:3000/
```

## Live Reload / Frontend Refresh

This project includes `django-livereload-server` support for local development.

- Make sure `DEBUG=True` in `.env`.
- Run the Django app on port 3000.
- Run the `livereload` management command in a second terminal.
- The livereload middleware injects `livereload.js` into HTML pages, and the livereload server watches templates and static files.
- When you save frontend files, the browser should auto-refresh or reflect the latest files after a normal reload.

If CSS/JS still appears stale, do a hard refresh in the browser:

```powershell
Ctrl+F5
```

If you prefer, you can also start the application with the livereload-aware command on the same terminal:

```powershell
python manage.py runserver 3000
```

and keep the separate `python manage.py livereload` terminal running to serve the livereload socket.

## Verifying Static Files (CSS / JS / Images)

During local development Django only serves static files automatically when `DEBUG=True`. If CSS or images are missing:

- Confirm `DEBUG=True` in the `.env` file used by the app.
- Confirm `STATIC_URL`, `STATICFILES_DIRS`, and `STATIC_ROOT` in `procurepro_project/settings.py`.
- Confirm the file exists on disk, e.g. `static/css/styles.css`.

To quickly test a static URL from the host machine:

```powershell
# From the project machine
Invoke-WebRequest -Uri "http://127.0.0.1:3000/static/css/styles.css" -UseBasicParsing
```

If you get a 404 and `DEBUG=True`, check the project `urls.py` includes the development static route (this project includes a conditional static route when `settings.DEBUG` is true).

## Production Notes (serving static files)

In production you should collect static files to `STATIC_ROOT` and serve them from your web server or CDN. Example:

```powershell
python manage.py collectstatic --noinput
# Then configure your webserver (nginx, Apache, etc.) to serve files from the STATIC_ROOT directory
```

For a simple production-ready option inside Django, consider using `whitenoise` to serve static files from the WSGI app.

## Common Troubleshooting

- Port 3000 already in use:

```powershell
# Show processes using port 3000
netstat -ano | findstr :3000
# Kill a process by PID
taskkill /PID <pid> /F
```

- Static files 404 but exist on disk:
  - Check `DEBUG` (development) or `collectstatic` (production).
  - Confirm templates use `{% load static %}` and `{% static 'css/styles.css' %}`.
  - Confirm file names and paths are exact (case sensitivity matters on Linux).

- Permission errors when uploading documents:
  - Make sure the `media/` directory exists and is writable by the process running Django.

## Useful Commands

```powershell
# Run tests
python manage.py test

# Check Django settings
python -c "import os, django; os.environ.setdefault('DJANGO_SETTINGS_MODULE','procurepro_project.settings'); django.setup(); from django.conf import settings; print(settings.DEBUG, settings.STATIC_URL, settings.STATICFILES_DIRS)"
```

## Next Steps

- Document major user flows in `docs/` or `PROJECT_OVERVIEW.md`.
- If you want, I can run the server here and verify static assets load, or implement WhiteNoise for production static serving.

---
Created by the project maintainer assistant. If you want any of these steps automated (virtualenv creation, dependency pinning, or CI integration), tell me which to add next.
