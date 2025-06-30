#!/bin/bash

# Algo Trading Platform Stop Script
# This script stops both the backend and frontend servers

echo "🛑 Stopping Algorithmic Trading Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Kill processes by PID if available
if [ -f "logs/server.pids" ]; then
    source logs/server.pids
    if [ ! -z "$BACKEND_PID" ]; then
        kill -TERM $BACKEND_PID 2>/dev/null || true
        print_status "Stopped backend server (PID: $BACKEND_PID)"
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill -TERM $FRONTEND_PID 2>/dev/null || true
        print_status "Stopped frontend server (PID: $FRONTEND_PID)"
    fi
    rm -f logs/server.pids
fi

# Kill any remaining processes
print_status "Cleaning up remaining processes..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
pkill -f "python3 app.py" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true
pkill -f "react-scripts start" 2>/dev/null || true

# Clean up PID files
rm -f logs/backend.pid logs/frontend.pid

print_success "All servers stopped successfully!"
echo "📋 Server logs are still available in the logs/ directory"