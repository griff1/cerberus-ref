#!/bin/bash
# Setup script for Cerberus Reference Implementation

echo "Setting up Cerberus Reference Implementation..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate

# Check Django configuration
echo ""
echo "Checking Django configuration..."
python manage.py check

echo ""
echo "========================================="
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. (Optional) Create a superuser:"
echo "   python manage.py createsuperuser"
echo ""
echo "3. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "4. Access the API at:"
echo "   http://localhost:8000/api/"
echo ""
echo "5. Test with:"
echo "   curl http://localhost:8000/api/health/"
echo "========================================="
