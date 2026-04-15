#!/bin/bash
# Installation script for Smart File Organizer (Linux/Mac)

echo "🚀 Installing Smart File Organizer..."
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Create virtual environment (optional but recommended)
read -p "Create virtual environment? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "✅ Virtual environment activated"
fi

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create logs directory
echo ""
echo "Creating logs directory..."
mkdir -p logs

# Run tests
echo ""
read -p "Run tests to verify installation? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
    echo "Running tests..."
    pytest tests/ -v
fi

# Test CLI
echo ""
echo "Testing CLI..."
python main.py --help

echo ""
echo "✅ Installation complete!"
echo ""
echo "Quick start:"
echo "  python main.py organize <path>"
echo "  python main.py --help"
echo ""
echo "Documentation:"
echo "  README.md - Full documentation"
echo "  QUICKSTART.md - Quick start guide"
echo "  USAGE_EXAMPLES.md - Real-world examples"
echo ""
