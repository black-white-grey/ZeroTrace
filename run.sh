#!/bin/bash
# Quick run script for ZeroTrace

echo "🔒 Starting ZeroTrace..."
echo ""

# Check if in correct directory
if [ ! -f "app.py" ]; then
    echo "❌ Error: Please run this script from the zerotrace directory"
    exit 1
fi

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Running setup..."
    pip install -r requirements.txt
fi

# Check Ollama
if command -v ollama &> /dev/null; then
    if ollama list 2>/dev/null | grep -q "llama3"; then
        echo "✅ Ollama with llama3 is ready"
    else
        echo "⚠️  llama3 model not found. AI action plans will be unavailable."
        echo "   Run: ollama pull llama3"
    fi
else
    echo "ℹ️  Ollama not found. AI action plans will be unavailable."
fi

echo ""
echo "🚀 Launching ZeroTrace..."
echo ""
echo "Sample data available:"
echo "  - CVE Database: data/sample_cves.json"
echo "  - Asset Inventory: data/sample_assets.csv"
echo ""
echo "Press Ctrl+C to stop"
echo ""

streamlit run app.py
