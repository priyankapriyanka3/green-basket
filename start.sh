#!/bin/bash
# start.sh — Start the GreenBasket AI full-stack application
set -e
trap 'echo "Shutting down..."; [ -f .pids ] && while IFS= read -r pid; do kill "$pid" 2>/dev/null || true; done < .pids; rm -f .pids; exit 0' SIGINT SIGTERM

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Convert path to native Windows format when running under Git Bash
native_path() {
    if command -v cygpath >/dev/null 2>&1; then
        cygpath -m "$1"
    else
        printf '%s' "$1"
    fi
}

# Port detection (lsof on macOS/Linux, netstat under Git Bash on Windows)
port_in_use() {
    if command -v lsof >/dev/null 2>&1; then
        lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null 2>&1
    else
        netstat -an 2>/dev/null | grep -Eq "[:.]$1[[:space:]].*LISTEN"
    fi
}

find_available_port() {
    local port=$1
    while port_in_use "$port"; do
        echo "  Port $port in use, trying $((port+1))..." >&2
        port=$((port+1))
    done
    echo $port
}

# === Prerequisite checks ===
check_prerequisites() {
    local errors=0
    echo "=== Checking prerequisites ==="

    # Probe by running it: under Git Bash `python3` may be the Windows Store stub.
    PYTHON=""
    for c in python3 python; do
        if "$c" -c 'import sys' >/dev/null 2>&1; then PYTHON=$c; break; fi
    done
    if [ -n "$PYTHON" ]; then
        PYTHON_VERSION=$("$PYTHON" -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
        PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
        PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 11 ]); then
            echo "❌ Python 3.11+ required (found $PYTHON_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Python $PYTHON_VERSION"
        fi
    else
        echo "❌ Python 3 not found. Install from https://python.org"
        errors=$((errors+1))
    fi

    if command -v node &>/dev/null; then
        NODE_VERSION=$(node --version | sed 's/v//')
        NODE_MAJOR=$(echo $NODE_VERSION | cut -d. -f1)
        if [ "$NODE_MAJOR" -lt 18 ]; then
            echo "❌ Node.js 18+ required (found $NODE_VERSION)"
            errors=$((errors+1))
        else
            echo "✓ Node.js $NODE_VERSION"
        fi
    else
        echo "❌ Node.js not found. Install from https://nodejs.org"
        errors=$((errors+1))
    fi

    if ! command -v npm &>/dev/null; then
        echo "❌ npm not found"
        errors=$((errors+1))
    else
        echo "✓ npm $(npm --version)"
    fi

    if [ $errors -gt 0 ]; then
        echo ""
        echo "❌ $errors prerequisite(s) missing. Please install them and retry."
        exit 1
    fi
    echo ""
}

check_prerequisites

# === Backend Setup ===
echo "=== Setting up backend ==="
cd backend

# Create venv if missing
if [ ! -d ".venv" ]; then
    echo "  Creating Python virtual environment..."
    "$PYTHON" -m venv .venv
fi

# Activate venv (Windows venvs have Scripts/, macOS/Linux venvs have bin/)
if [ -f .venv/Scripts/activate ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

# Install dependencies
echo "  Installing backend dependencies..."
pip install . -q

# Copy dev.env to .env if .env doesn't exist
if [ ! -f .env ]; then
    echo "  Creating .env from dev.env..."
    cp dev.env .env
fi

# Load DATABASE_URL from .env if it exists
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Default to SQLite if DATABASE_URL not set
if [ -z "$DATABASE_URL" ]; then
    DB_PATH="$SCRIPT_DIR/backend/app.db"
    export DATABASE_URL="sqlite:///$(native_path "$DB_PATH")"
fi

echo "  Database: $DATABASE_URL"

# Run migrations
echo "  Running database migrations..."
alembic upgrade head

# Seed database if empty
echo "  Seeding database..."
python seed_data.py 2>/dev/null || true

cd "$SCRIPT_DIR"

# === Frontend Setup ===
echo ""
echo "=== Setting up frontend ==="
cd frontend

echo "  Installing frontend dependencies..."
npm ci --silent

cd "$SCRIPT_DIR"

# === Port Detection ===
echo ""
echo "=== Detecting available ports ==="
BACKEND_PORT=$(find_available_port 8000)
FRONTEND_PORT=$(find_available_port 5173)
echo "  Backend port:  $BACKEND_PORT"
echo "  Frontend port: $FRONTEND_PORT"

# === Start Services ===
echo ""
echo "=== Starting services ==="

# Start backend
cd backend
echo "  Starting backend on http://localhost:$BACKEND_PORT"
uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload >/dev/null 2>&1 &
BACKEND_PID=$!
cd "$SCRIPT_DIR"

# Wait a moment for backend to initialize
sleep 2

# Start frontend (BACKEND_PORT env var is read by vite.config.ts proxy)
cd frontend
echo "  Starting frontend on http://localhost:$FRONTEND_PORT"
BACKEND_PORT="$BACKEND_PORT" npm run dev -- --port "$FRONTEND_PORT" >/dev/null 2>&1 &
FRONTEND_PID=$!
cd "$SCRIPT_DIR"

# Save PIDs for stop.sh
echo "$BACKEND_PID" > .pids
echo "$FRONTEND_PID" >> .pids

# === Startup Summary ===
echo ""
echo "=============================================="
echo "  GreenBasket AI - Running"
echo "=============================================="
echo ""
echo "URLs:"
echo "  Frontend:  http://localhost:$FRONTEND_PORT"
echo "  Backend:   http://localhost:$BACKEND_PORT"
echo "  API Docs:  http://localhost:$BACKEND_PORT/api/docs"
echo ""
echo "Demo Credentials:"
echo "  Ananya (Shopper):"
echo "    Phone:    +919876543210"
echo "    Password: Demo@123"
echo ""
echo "  Rohan (Operator):"
echo "    Phone:    +919876543220"
echo "    Password: Demo@123"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=============================================="
echo ""

# Wait for processes
wait
