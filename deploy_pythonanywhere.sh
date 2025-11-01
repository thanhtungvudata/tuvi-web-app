#!/bin/bash

# Deploy script for PythonAnywhere
# This script automates the deployment process for the Tuvi Web App on PythonAnywhere

echo "=========================================="
echo "PythonAnywhere Deployment Script"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

# Step 1: Pull latest changes from GitHub
print_info "Step 1: Pulling latest changes from GitHub..."
git pull origin main
if [ $? -eq 0 ]; then
    print_success "Successfully pulled latest changes"
else
    print_error "Failed to pull changes from GitHub"
    exit 1
fi
echo ""

# Step 2: Activate virtual environment (if running locally)
if [ -d ".venv" ]; then
    print_info "Step 2: Activating virtual environment..."
    source .venv/bin/activate
    print_success "Virtual environment activated"
else
    print_info "Step 2: No local virtual environment found, skipping..."
fi
echo ""

# Step 3: Install/Update dependencies
print_info "Step 3: Installing/Updating dependencies..."
pip install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    exit 1
fi
echo ""

# Step 4: Run database migrations
print_info "Step 4: Running database migrations..."
python manage.py makemigrations
python manage.py migrate
if [ $? -eq 0 ]; then
    print_success "Migrations completed successfully"
else
    print_error "Failed to run migrations"
    exit 1
fi
echo ""

# Step 5: Clean old static files and collect new ones
print_info "Step 5: Cleaning old static files..."
rm -rf staticfiles/tuvi
print_success "Old static files removed"
echo ""

print_info "Step 6: Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    print_success "Static files collected successfully"
else
    print_error "Failed to collect static files"
    exit 1
fi
echo ""

# Step 7: Instructions for PythonAnywhere
echo "=========================================="
print_success "Local deployment steps completed!"
echo "=========================================="
echo ""
echo "Next steps for PythonAnywhere (manual):"
echo ""
echo "1. Go to PythonAnywhere Web tab:"
echo "   https://www.pythonanywhere.com/user/thanhtungvu/webapps/"
echo ""
echo "2. Click 'Reload thanhtungvu.pythonanywhere.com' button"
echo ""
echo "3. If you need to run these commands on PythonAnywhere console:"
echo "   $ cd ~/tuvi_web_app"
echo "   $ git pull origin main"
echo "   $ source .venv/bin/activate"
echo "   $ pip install -r requirements.txt"
echo "   $ python manage.py migrate"
echo "   $ rm -rf staticfiles/tuvi"
echo "   $ python manage.py collectstatic --noinput"
echo ""
echo "4. Then reload the web app from the Web tab"
echo ""
print_success "Deployment preparation complete!"
