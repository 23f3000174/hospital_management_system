#!/bin/bash

# HMS - Start All Services with Logging
# Run this from the project root: bash start.sh

BACKEND_DIR="$(cd "$(dirname "$0")/backend" && pwd)"
FRONTEND_DIR="$(cd "$(dirname "$0")/frontend" && pwd)"
VENV="$BACKEND_DIR/.env/bin/activate"

# Create a logs directory
LOGS_DIR="$(cd "$(dirname "$0")" && pwd)/logs"
mkdir -p "$LOGS_DIR"

echo "================================================"
echo "  Hospital Management System - Starting All"
echo "  Logs will be saved to: ./logs/"
echo "================================================"

# Check if Redis is running
if redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is already running"
else
    echo "🔄 Starting Redis..."
    redis-server --daemonize yes
    sleep 1
    if redis-cli ping > /dev/null 2>&1; then
        echo "✅ Redis started"
    else
        echo "❌ Failed to start Redis. Start it manually: redis-server"
        exit 1
    fi
fi

# Check if MailHog is running on port 8025 (Web GUI)
if curl -s http://localhost:8025 > /dev/null 2>&1; then
    echo "✅ MailHog already running on port 8025/1025"
else
    echo "🔄 Starting MailHog..."
    # Assuming MailHog is installed via Go in the user's home dir
    ~/go/bin/MailHog > "$LOGS_DIR/mailhog.log" 2>&1 &
    MAIL_PID=$!
    echo "✅ MailHog started (PID: $MAIL_PID) -> logs/mailhog.log"
fi

# Kill any existing Flask on port 5000
if lsof -t -i:5000 > /dev/null 2>&1; then
    echo "🔄 Killing existing Flask on port 5000..."
    kill $(lsof -t -i:5000) 2>/dev/null
    sleep 1
fi

# Start Flask backend
echo "🔄 Starting Flask backend..."
source "$VENV"
cd "$BACKEND_DIR"
python app.py > "$LOGS_DIR/flask.log" 2>&1 &
FLASK_PID=$!
echo "✅ Flask started (PID: $FLASK_PID) -> logs/flask.log"
sleep 2

# Start Celery Worker
echo "🔄 Starting Celery Worker..."
celery -A celery_app worker --loglevel=info > "$LOGS_DIR/celery_worker.log" 2>&1 &
CELERY_PID=$!
echo "✅ Celery Worker started (PID: $CELERY_PID) -> logs/celery_worker.log"

# Start Celery Beat
echo "🔄 Starting Celery Beat..."
celery -A celery_app beat --loglevel=info > "$LOGS_DIR/celery_beat.log" 2>&1 &
BEAT_PID=$!
echo "✅ Celery Beat started (PID: $BEAT_PID) -> logs/celery_beat.log"
sleep 1

# Start Frontend
echo "🔄 Starting Frontend..."
cd "$FRONTEND_DIR"
npm run dev > "$LOGS_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "✅ Frontend started (PID: $FRONTEND_PID) -> logs/frontend.log"

echo ""
echo "================================================"
echo "  All Services Running!"
echo "================================================"
echo "  Flask:    http://127.0.0.1:5000"
echo "  Frontend: http://localhost:5173"
echo "  MailHog:  http://localhost:8025"
echo ""
echo "  To view logs while it's running, open a new terminal and run:"
echo "    tail -f logs/flask.log          # API errors/requests"
echo "    tail -f logs/celery_worker.log  # Background task logs"
echo "    tail -f logs/frontend.log       # Vue.js build/errors"
echo ""
echo "  Press Ctrl+C to stop all services"
echo "================================================"

# Trap Ctrl+C to kill all background processes
cleanup() {
    echo ""
    echo "🛑 Stopping all services..."
    kill $FLASK_PID $CELERY_PID $BEAT_PID $FRONTEND_PID $MAIL_PID 2>/dev/null
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Wait for all background processes to keep terminal open
wait
