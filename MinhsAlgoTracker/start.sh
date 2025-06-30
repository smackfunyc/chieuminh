#!/bin/bash

# Algo Trading Platform Startup Script
# This script starts both the backend and frontend servers

set -e  # Exit on any error

echo "🚀 Starting Algorithmic Trading Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8+ to continue."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 16+ to continue."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm to continue."
    exit 1
fi

print_status "Checking system requirements..."
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
NODE_VERSION=$(node --version)
print_success "Python version: $PYTHON_VERSION"
print_success "Node.js version: $NODE_VERSION"

# Kill any existing processes on ports 3000 and 5001
print_status "Cleaning up existing processes..."
lsof -ti:3000 | xargs kill -9 2>/dev/null || true
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
pkill -f "python3 app.py" 2>/dev/null || true
pkill -f "npm start" 2>/dev/null || true

# Create necessary directories
print_status "Creating directories..."
mkdir -p uploads historical_data logs

# Setup Python virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install backend dependencies
print_status "Installing backend dependencies..."
cd backend
if [ ! -f ".deps_installed" ]; then
    print_status "Installing Python packages (this may take a few minutes)..."
    pip install --upgrade pip
    pip install -r requirements.txt
    touch .deps_installed
    print_success "Backend dependencies installed!"
else
    print_status "Backend dependencies already installed."
fi
cd ..

# Install frontend dependencies
print_status "Installing frontend dependencies..."
cd frontend
if [ ! -d "node_modules" ]; then
    print_status "Installing Node.js packages (this may take a few minutes)..."
    npm install
    print_success "Frontend dependencies installed!"
else
    print_status "Frontend dependencies already installed."
fi
cd ..

# Create .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    print_status "Creating environment configuration..."
    cp backend/.env.example backend/.env
    print_warning "Please edit backend/.env with your API keys if needed."
fi

# Start backend server
print_status "Starting backend server..."
cd backend
source ../venv/bin/activate
python3 app.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
cd ..

# Wait for backend to start
print_status "Waiting for backend to initialize..."
sleep 5

# Check if backend is running
if curl -s http://localhost:5001/api/portfolio > /dev/null; then
    print_success "Backend server started successfully on http://localhost:5001"
else
    print_error "Backend failed to start. Check logs/backend.log for details."
    exit 1
fi

# Start frontend server
print_status "Starting frontend server..."
cd frontend
npm start > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..

# Wait for frontend to start
print_status "Waiting for frontend to initialize..."
sleep 10

# Check if frontend is running
if curl -s http://localhost:3000 > /dev/null; then
    print_success "Frontend server started successfully on http://localhost:3000"
else
    print_error "Frontend failed to start. Check logs/frontend.log for details."
    exit 1
fi

echo ""
echo "🎉 ================================="
echo "🚀 ALGORITHMIC TRADING PLATFORM IS READY!"
echo "🎉 ================================="
echo ""
echo "📱 Frontend (Web Interface): http://localhost:3000"
echo "🔧 Backend API:              http://localhost:5001"
echo ""
echo "📊 Features Available:"
echo "   • Trading Dashboard - Portfolio monitoring & script control"
echo "   • Script Manager - Upload Python trading strategies"
echo "   • Backtesting - Test strategies on historical data"
echo "   • API Keys - Configure exchange credentials"
echo "   • Real-Time Charts - Live market data with indicators"
echo ""
echo "📝 Sample Scripts Available:"
echo "   • examples/sma_strategy.py - Simple Moving Average strategy"
echo "   • examples/rsi_strategy.py - RSI mean reversion strategy"
echo ""
echo "🛑 To stop the servers, run: ./stop.sh"
echo "📋 View logs: tail -f logs/backend.log logs/frontend.log"
echo ""
echo "🌐 Open your browser and navigate to: http://localhost:3000"
echo ""

# Store PIDs for cleanup
echo "BACKEND_PID=$BACKEND_PID" > logs/server.pids
echo "FRONTEND_PID=$FRONTEND_PID" >> logs/server.pids

# Wait and keep script running
echo "Press Ctrl+C to stop all servers..."
trap 'echo ""; echo "🛑 Stopping servers..."; ./stop.sh; exit' INT

# Keep script running
while true; do
    sleep 1
done