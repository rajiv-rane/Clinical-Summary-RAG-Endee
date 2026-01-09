#!/bin/bash
# Startup script to run both FastAPI and Streamlit services

set -e

echo "============================================================"
echo "🚀 Starting Clinical Summary RAG Application"
echo "============================================================"

# Check if GROQ_API_KEY is set
if [ -z "$GROQ_API_KEY" ]; then
    echo "⚠️  WARNING: GROQ_API_KEY environment variable is not set!"
    echo "   The application may not work correctly."
fi

# Get port from environment variable (Railway/Render sets this)
# Use PORT for Streamlit (main service), FastAPI on internal port
EXTERNAL_PORT=${PORT:-8501}
FASTAPI_PORT=${FASTAPI_PORT:-8000}

# For Railway/Render: PORT is the external port, use internal port for FastAPI
# FastAPI will run on 8000 internally, Streamlit on the assigned PORT
echo "📍 FastAPI will run on port: $FASTAPI_PORT (internal)"
echo "📍 Streamlit will run on port: $EXTERNAL_PORT (external)"
echo "============================================================"

# Set FastAPI URL for Streamlit to connect
export FASTAPI_URL="http://localhost:$FASTAPI_PORT"

# Function to handle shutdown
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill $FASTAPI_PID $STREAMLIT_PID 2>/dev/null || true
    wait
    echo "✅ Services stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGTERM SIGINT

# Start FastAPI in background
echo "⏳ Starting FastAPI backend..."
cd /app
python -m uvicorn api:app \
    --host 0.0.0.0 \
    --port $FASTAPI_PORT \
    --log-level info \
    --workers 1 \
    --no-reload &
FASTAPI_PID=$!

# Wait a bit for FastAPI to start
echo "⏳ Waiting for FastAPI to initialize..."
sleep 8

# Start Streamlit in foreground (this will be the main process)
echo "⏳ Starting Streamlit frontend..."
echo "============================================================"
echo "✅ FastAPI is running on port $FASTAPI_PORT"
echo "📍 Starting Streamlit on port $EXTERNAL_PORT"
echo "============================================================"
echo ""
echo "⏳ Application is loading..."
echo "   (This may take 1-2 minutes for model loading on first start)"
echo ""

# Set Streamlit environment variables
export STREAMLIT_SERVER_PORT=$EXTERNAL_PORT
export STREAMLIT_SERVER_ADDRESS=0.0.0.0
export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Run Streamlit in foreground (Railway needs a foreground process)
streamlit run app.py \
    --server.port=$EXTERNAL_PORT \
    --server.address=0.0.0.0 \
    --server.headless=true \
    --browser.gatherUsageStats=false

# If Streamlit exits, cleanup
cleanup
