#!/bin/bash

# Bobyard Comment System - Backend Setup Script
# This script automates the initial setup of the Django backend

set -e  # Exit on error

echo "🚀 Bobyard Comment System - Backend Setup"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"

# Check if PostgreSQL is installed
if ! command -v psql &> /dev/null; then
    echo "⚠️  PostgreSQL not found. Please ensure PostgreSQL is installed and running."
    echo "   Download from: https://www.postgresql.org/download/"
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ .env file created. Please update it with your database credentials."
    echo ""
    echo "📝 Edit .env file now? (y/n)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
        ${EDITOR:-nano} .env
    fi
fi

# Database setup instructions
echo ""
echo "📊 Database Setup"
echo "================="
echo "Make sure PostgreSQL is running and you have created the database:"
echo ""
echo "  psql -U postgres"
echo "  CREATE DATABASE comments_db;"
echo "  \q"
echo ""
echo "Press Enter when ready to continue..."
read

# Run migrations
echo ""
echo "🔄 Running database migrations..."
python manage.py makemigrations
python manage.py migrate
echo "✅ Migrations completed"

# Create superuser prompt
echo ""
echo "👤 Create admin superuser? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python manage.py createsuperuser
fi

# Load initial data
echo ""
echo "📂 Load sample comments from JSON? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    if [ -f "data/comments.json" ]; then
        python manage.py load_comments
        echo "✅ Sample data loaded"
    else
        echo "⚠️  data/comments.json not found"
    fi
fi

# Collect static files (for production)
echo ""
echo "📁 Collect static files? (y/n)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    python manage.py collectstatic --noinput
    echo "✅ Static files collected"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "  1. Make sure your .env file has correct database credentials"
echo "  2. Start the development server: python manage.py runserver"
echo "  3. Access the API at: http://localhost:8000/api/comments/"
echo "  4. Access admin panel at: http://localhost:8000/admin/"
echo ""
echo "Happy coding! 🎉"

