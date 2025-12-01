# Cerberus Reference Implementation

A simple Django REST API that demonstrates integration with the Cerberus middleware for testing purposes. This reference implementation provides basic CRUD endpoints without authentication to validate Cerberus metrics collection.

## Quick Start

### 1. Setup Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Database Migrations

```bash
# Create database tables
python manage.py migrate

# (Optional) Create admin user for Django admin interface
python manage.py createsuperuser
```

### 3. Configure Cerberus

The application is pre-configured to work with a local Cerberus backend. Update the configuration in `cerberus_ref/settings.py` or use environment variables:

```bash
# Set your Cerberus API key
export CERBERUS_API_KEY="your-api-key-here"

# Set the backend URL (default: http://localhost:8001)
export CERBERUS_BACKEND_URL="http://localhost:8001"
```

### 4. Start the Server

```bash
# Start Django development server
python manage.py runserver

# Or run on a different port
python manage.py runserver 8080
```

The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Health Check
```bash
GET /api/health/
```

### Metrics Example
Demonstrates custom Cerberus metrics:
```bash
GET /api/metrics-example/
```

### Items CRUD
```bash
GET    /api/items/           # List all items
POST   /api/items/           # Create new item
GET    /api/items/{id}/      # Get item details
PUT    /api/items/{id}/      # Update item
DELETE /api/items/{id}/      # Delete item
```

### Testing Endpoints
```bash
GET /api/slow/                    # Slow endpoint (0.5-2s delay)
GET /api/error/?type=validation   # Error example (400)
GET /api/error/?type=not_found    # Error example (404)
GET /api/error/?type=server       # Error example (500)
```

## Example Usage

### Create an Item
```bash
curl -X POST http://localhost:8000/api/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Item", "description": "A test item", "quantity": 5}'
```

### List Items
```bash
curl http://localhost:8000/api/items/
```

### Get Metrics Example
```bash
curl http://localhost:8000/api/metrics-example/
```

## Running Tests

```bash
# Run all tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report

# Run specific test
python manage.py test api.tests.ItemAPITestCase
```

## Cerberus Integration

This application uses the Cerberus middleware to collect and send HTTP request metrics. The middleware:

1. Intercepts all incoming requests
2. Captures metadata (IP, endpoint, method, scheme)
3. Extracts custom metrics from responses (if present)
4. Sends data asynchronously to the backend via TCP

### Custom Metrics

Views can attach custom metrics to responses:

```python
@api_view(['GET'])
def my_view(request):
    response = Response({'data': 'value'})

    # Add custom metrics for Cerberus
    response.data['_cerberus_metrics'] = {
        'processing_time_ms': 123,
        'cache_hit': True,
        'items_processed': 42
    }

    return response
```

The middleware automatically extracts `_cerberus_metrics` and includes it in the data sent to the backend.

## Development

### Code Quality

```bash
# Format code with black
black .

# Lint with flake8
flake8 .

# Check Django configuration
python manage.py check
```

### Database Management

```bash
# Make migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (SQLite only)
rm db.sqlite3
python manage.py migrate
```

## Project Structure

```
cerberus-ref/
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database (gitignored)
├── cerberus_ref/         # Django project directory
│   ├── settings.py       # Settings (includes CERBERUS_CONFIG)
│   ├── urls.py          # URL routing
│   ├── wsgi.py          # WSGI application
│   └── asgi.py          # ASGI application
└── api/                 # API app
    ├── models.py        # Database models
    ├── views.py         # API endpoints
    ├── serializers.py   # DRF serializers
    ├── urls.py          # App URL routing
    ├── admin.py         # Django admin configuration
    └── tests.py         # Test cases
```

## Related Repositories

- **Cerberus Middleware**: `~/Documents/cerberus` - The Django middleware package
- **Cerberus Backend**: `~/Documents/cerberus-int` - The event processing backend

See `CLAUDE.md` for detailed architecture and development information.
