#!/bin/bash
# ZeroTrace Quick Setup Script

echo "🔒 ZeroTrace Setup"
echo "=================="
echo ""

# Check Python version
echo "Checking Python version..."
python --version

if [ $? -ne 0 ]; then
    echo "❌ Python not found. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found"
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Check if Ollama is installed
echo "Checking for Ollama..."
if command -v ollama &> /dev/null; then
    echo "✅ Ollama found"
    
    # Check if llama3 is available
    if ollama list | grep -q "llama3"; then
        echo "✅ Llama3 model found"
    else
        echo "⚠️  Llama3 model not found. Installing..."
        ollama pull llama3
    fi
else
    echo "⚠️  Ollama not found. AI action plans will not be available."
    echo "   Install Ollama from: https://ollama.ai/"
fi

echo ""
echo "🚀 Setup complete!"
echo ""
echo "To start ZeroTrace, run:"
echo "  streamlit run app.py"
echo ""
echo "Sample data available:"
echo "  - CVE database: data/sample_cves.json (21 CVEs)"
echo "  - Asset inventory: data/sample_assets.csv (15 assets)"
echo ""
