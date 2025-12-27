# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a reference implementation of a Django API that integrates the Cerberus middleware for testing purposes. The application provides simple REST endpoints without authentication and demonstrates proper integration of the Cerberus monitoring middleware.

**Purpose:** Provide a minimal, testable Django application that can be used to validate Cerberus middleware functionality and backend event processing.

## Architecture

### Core Components

**Django Application:**
- Simple REST API with Django Rest Framework (DRF)
- Basic endpoints for testing Cerberus metrics collection
- No authentication required (testing/reference only)
- Cerberus middleware intercepts all requests and sends metrics to backend

**Cerberus Middleware Integration:**
- Located in `../cerberus/src/cerberus-django/` (separate repository)
- Imported via wrapper (`cerberus_ref/cerberus_middleware.py`) due to hyphens in source package name
- Middleware captures HTTP request metadata (IP, endpoint, method, scheme)
- Sends data asynchronously via TCP to backend analytics server
- Automatically fetches HMAC secret key for PII pseudoanonymization
- Backend server: `../cerberus-int/services/event_ingest/` (separate repository)

**Implementation Note:** The Cerberus middleware source uses `cerberus-django` (with hyphens) as the package name, which cannot be directly imported in Python. The file `cerberus_ref/cerberus_middleware.py` uses `importlib` to dynamically load the middleware from the source directory.

**Data Flow:**
1. Client makes HTTP request to Django API
2. Django processes request through views
3. `CerberusMiddleware` intercepts request/response
4. Metrics queued to async queue with optional custom data
5. Background task sends JSON data via TCP to backend server
6. Backend validates, processes, and stores in Kafka/PostgreSQL

### Custom Metrics Pattern

Views can attach custom metrics to responses for inclusion in Cerberus analytics:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def my_endpoint(request):
    result = {"message": "Success"}

    # Add custom metrics (will be extracted and sent to Cerberus)
    cerberus_metrics = {
        "items_processed": 42,
        "cache_hit": True,
        "processing_time_ms": 123
    }

    response = Response(result)
    response.data['_cerberus_metrics'] = cerberus_metrics
    return response
```

The middleware automatically extracts `_cerberus_metrics` from the response and includes it in the `CoreData.custom_data` field before sending to the backend.

## Development Commands

### Environment Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv/bin/activate.fish for fish shell

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser (optional, for admin interface)
python manage.py createsuperuser
```

### Running the Server

```bash
# Development server (default port 8000)
python manage.py runserver

# Run on specific port
python manage.py runserver 8080

# Run on all interfaces
python manage.py runserver 0.0.0.0:8000
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test myapp

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generates htmlcov/index.html

# Run specific test file
python manage.py test myapp.tests.test_views
```

### Database Management

```bash
# Make migrations for model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations

# Reset database (SQLite only)
rm db.sqlite3
python manage.py migrate
```

### Code Quality

```bash
# Format code with black
black .

# Lint with flake8
flake8 .

# Check Django configuration
python manage.py check
```

## Configuration

### Cerberus Middleware Configuration

Add to `settings.py`:

```python
MIDDLEWARE = [
    # ... other middleware
    'cerberus_django.middleware.CerberusMiddleware',  # Add this
]

# Cerberus configuration
CERBERUS_CONFIG = {
    # Option 1: Auto-fetch secret key from backend (recommended)
    'token': 'your-api-key-here',  # API key from cerberus-int backend
    'backend_url': 'http://localhost:8001',  # URL to event_ingest service

    # Option 2: Manual secret key (if backend_url not set)
    # 'secret_key': 'your-hmac-secret-key',  # For PII hashing
}
```

**Configuration Details:**
- `token`: API key for authenticating with the Cerberus backend (required)
- `backend_url`: HTTP URL to fetch the shared HMAC secret key from `/api/secret-key` endpoint
- `secret_key`: Manually configured HMAC key (only if `backend_url` not provided)
- If `backend_url` is configured, middleware will automatically fetch `secret_key` at startup
- If neither `backend_url` nor `secret_key` is provided, PII will not be hashed (warning logged)

**PII Pseudoanonymization:**
The middleware uses HMAC-SHA256 to hash PII fields (currently `source_ip`) before transmission. The same IP will always hash to the same value with a given key, enabling privacy-preserving analytics.

### Important Settings

```python
# Django settings for reference implementation
DEBUG = True  # Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# CORS (if needed for frontend testing)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]

# Database (default SQLite for testing)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

## Related Repositories

This reference implementation integrates with two separate repositories co-located in the parent directory. See their respective CLAUDE.md files for details.

### Cerberus Middleware (`../cerberus/`)

Django middleware package for instrumenting applications.

**Key Files:**
- `src/cerberus-django/middleware.py` - Main middleware implementation
- `src/cerberus-django/structs.py` - `CoreData` dataclass definition
- `src/cerberus-django/utils.py` - PII hashing and secret key fetching utilities

See `../cerberus/CLAUDE.md` for detailed middleware documentation.

### Cerberus Backend (`../cerberus-int/`)

Backend infrastructure and microservices for event processing (optional - can use any compatible backend).

**Event Ingest Service:**
- FastAPI WebSocket server on port 8001 (default)
- Provides `/api/secret-key` endpoint for HMAC key
- Validates API keys and publishes to Kafka

See `../cerberus-int/CLAUDE.md` for detailed backend documentation.

## Testing Cerberus Integration

### Running Backend Locally

Before testing the Django reference app, start the Cerberus backend (optional - only if testing full integration):

```bash
# Terminal 1: Start event_ingest service
cd ../cerberus-int/services/event_ingest
source venv/bin/activate
python main.py

# Terminal 2: Start Django reference app (from cerberus-ref directory)
source venv/bin/activate
python manage.py runserver
```

### Verifying Metrics Collection

1. Make requests to Django API endpoints
2. Check Django console for Cerberus middleware logs
3. Check event_ingest service logs for received metrics
4. Query PostgreSQL `events` table to verify storage

### Common Test Scenarios

**Basic Request Tracking:**
```bash
curl http://localhost:8000/api/test/
# Middleware captures: source_ip, endpoint="/api/test/", method="GET", scheme=false
```

**Custom Metrics:**
```bash
curl http://localhost:8000/api/metrics-example/
# View returns response with _cerberus_metrics
# Middleware extracts and includes in custom_data field
```

## File Structure

```
cerberus-ref/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database (gitignored)
├── myproject/            # Django project directory
│   ├── settings.py       # Django settings (includes CERBERUS_CONFIG)
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
└── myapp/               # Example Django app
    ├── models.py        # Database models
    ├── views.py         # API endpoints
    ├── urls.py          # App URL routing
    └── tests.py         # Test cases
```

## Important Notes

- This is a reference implementation for testing - not production-ready
- No authentication/authorization implemented (add for production use)
- Uses SQLite by default (switch to PostgreSQL for production)
- Cerberus middleware sends metrics via TCP - ensure backend TCP listener is running
- The middleware is designed for ASGI but has WSGI fallback support
- API keys and secrets should be stored in environment variables, not hardcoded
- PII hashing requires shared HMAC secret key from backend or manual configuration
