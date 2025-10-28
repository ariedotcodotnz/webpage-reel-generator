#!/bin/bash
# Setup script for Webpage Reel Generator

echo "🚀 Setting up Webpage Reel Generator..."
echo "======================================"

# Check Python version
python3 --version
if [ $? -ne 0 ]; then
    echo "❌ Python 3 is required but not found"
    exit 1
fi

# Install system dependencies
echo ""
echo "📦 Installing system dependencies..."
if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y chromium-browser chromium-chromedriver fonts-dejavu-core
elif command -v yum &> /dev/null; then
    sudo yum install -y chromium chromedriver dejavu-sans-fonts
elif command -v brew &> /dev/null; then
    brew install --cask chromium
    brew install chromedriver
else
    echo "⚠️  Please install Chromium and ChromeDriver manually"
fi

# Install Python dependencies
echo ""
echo "🐍 Installing Python dependencies..."
pip3 install --break-system-packages -r requirements.txt

echo ""
echo "✅ Setup complete!"
echo ""
echo "Usage:"
echo "  python3 webpage_reel_generator.py <URL>"
echo ""
echo "Example:"
echo "  python3 webpage_reel_generator.py https://example.com"
echo ""
