#!/bin/bash

echo "======================================================================"
echo "N8N Template Extractor - Quick Start"
echo "======================================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip."
    exit 1
fi

echo "✓ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
python3 -m playwright install chromium

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Playwright browsers"
    echo "Try running: playwright install-deps"
    exit 1
fi

echo "✓ Playwright browsers installed"

# Run the extractor
echo ""
echo "🚀 Starting extraction process..."
echo ""
python3 extract_n8n_templates.py

echo ""
echo "======================================================================"
echo "✓ Extraction complete! Check the n8n_templates/ directory"
echo "======================================================================"
