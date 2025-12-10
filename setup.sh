#!/bin/bash

echo "============================================"
echo "  LensLock Pro - Setup Script"
echo "============================================"
echo ""

echo "Step 1: Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d ' ' -f 2 | cut -d '.' -f 1,2)
echo "Found Python $PYTHON_VERSION"
echo ""

echo "Step 2: Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created!"
else
    echo "Virtual environment already exists."
fi
echo ""

echo "Step 3: Activating virtual environment..."
source venv/bin/activate
echo "Virtual environment activated!"
echo ""

echo "Step 4: Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed!"
echo ""

echo "Step 5: Setting up directories..."
mkdir -p uploads
mkdir -p outputs
mkdir -p reports
echo "Directories created!"
echo ""

echo "Step 6: Environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo ".env file created from template."
    echo ""
    echo "IMPORTANT: Please edit .env and add your Supabase credentials:"
    echo "  - VITE_SUPABASE_URL"
    echo "  - VITE_SUPABASE_ANON_KEY"
    echo ""
else
    echo ".env file already exists."
fi
echo ""

echo "============================================"
echo "  Setup Complete!"
echo "============================================"
echo ""
echo "Next steps:"
echo "1. Configure your .env file with Supabase credentials"
echo "2. Run 'npm run dev' to start the development server"
echo "3. Open http://localhost:8000 in your browser"
echo ""
echo "For deployment instructions, see DEPLOYMENT.md"
echo ""
