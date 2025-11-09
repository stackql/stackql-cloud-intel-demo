#!/bin/bash

# StackQL Cloud Intelligence Demo Startup Script

set -e

echo "🚀 Starting StackQL Cloud Intelligence Demo"
echo "=========================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from template..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration and run this script again."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ] || [ "$OPENAI_API_KEY" = "your_openai_api_key_here" ]; then
    echo "❌ Error: OPENAI_API_KEY not set in .env file"
    echo "Please add your OpenAI API key to the .env file"
    exit 1
fi

echo "✅ Configuration loaded"

# Check if StackQL is installed
if ! command -v stackql &> /dev/null; then
    echo "⚠️  StackQL not found. You have two options:"
    echo ""
    echo "Option 1: Use Docker Compose (recommended)"
    echo "  docker-compose up -d"
    echo ""
    echo "Option 2: Install StackQL manually"
    echo "  Visit: https://stackql.io/docs"
    echo ""
    read -p "Would you like to use Docker Compose? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🐳 Starting services with Docker Compose..."
        docker-compose up -d
        echo ""
        echo "✅ Services started!"
        echo "📱 Chat interface: http://localhost:8501"
        echo "🔌 StackQL MCP: http://localhost:9912"
        echo ""
        echo "To view logs: docker-compose logs -f"
        echo "To stop: docker-compose down"
        exit 0
    else
        exit 1
    fi
fi

# Start StackQL MCP Server in background
echo "🔧 Starting StackQL MCP Server..."

# Build the auth configuration based on available credentials
AUTH_CONFIG=""

if [ ! -z "$GOOGLE_CREDENTIALS" ]; then
    AUTH_CONFIG="--auth={\"google\":{\"type\":\"service_account\",\"credentialsfilepath\":\"$GOOGLE_CREDENTIALS\"}}"
fi

# Start StackQL MCP server
nohup stackql mcp \
    --mcp.server.type=http \
    --mcp.config='{"server": {"transport": "http", "address": "127.0.0.1:9912"}}' \
    $AUTH_CONFIG \
    > stackql-mcp.log 2>&1 &

STACKQL_PID=$!
echo "✅ StackQL MCP Server started (PID: $STACKQL_PID)"
echo "📋 Logs: tail -f stackql-mcp.log"

# Wait for StackQL to be ready
echo "⏳ Waiting for StackQL MCP Server to be ready..."
for i in {1..30}; do
    if curl -s http://127.0.0.1:9912 > /dev/null 2>&1; then
        echo "✅ StackQL MCP Server is ready!"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install -q -r requirements.txt

# Start Streamlit app
echo "🌐 Starting Chat Interface..."
echo ""
echo "=========================================="
echo "✅ StackQL Cloud Intelligence Demo is ready!"
echo "=========================================="
echo ""
echo "📱 Chat Interface: http://localhost:8501"
echo "🔌 StackQL MCP Server: http://localhost:9912"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start Streamlit
streamlit run app.py

# Cleanup on exit
trap "echo '🛑 Stopping StackQL MCP Server...'; kill $STACKQL_PID 2>/dev/null" EXIT
