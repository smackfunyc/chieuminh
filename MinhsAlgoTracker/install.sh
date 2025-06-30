#!/bin/bash

# Algo Trading Platform Installation Script
# This script sets up the complete development environment

set -e  # Exit on any error

echo "🚀 Installing Algorithmic Trading Platform..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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

# Check operating system
OS="$(uname -s)"
case "${OS}" in
    Linux*)     MACHINE=Linux;;
    Darwin*)    MACHINE=Mac;;
    CYGWIN*)    MACHINE=Cygwin;;
    MINGW*)     MACHINE=MinGw;;
    *)          MACHINE="UNKNOWN:${OS}"
esac

print_status "Detected operating system: $MACHINE"

# Function to install Python dependencies
install_python_deps() {
    print_status "Installing Python dependencies..."
    
    # Check if we're on macOS and need to install TA-Lib
    if [ "$MACHINE" = "Mac" ]; then
        if ! command -v brew &> /dev/null; then
            print_warning "Homebrew not found. Please install TA-Lib manually:"
            print_warning "Visit: https://ta-lib.org/hdr_dw.html"
        else
            print_status "Installing TA-Lib via Homebrew..."
            brew install ta-lib || print_warning "TA-Lib installation failed. You may need to install it manually."
        fi
    elif [ "$MACHINE" = "Linux" ]; then
        print_status "Installing TA-Lib dependencies for Linux..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y libta-lib-dev
        elif command -v yum &> /dev/null; then
            sudo yum install -y ta-lib-devel
        else
            print_warning "Could not install TA-Lib automatically. Please install it manually."
        fi
    fi
}

# Check system requirements
print_status "Checking system requirements..."

# Check Python 3
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed!"
    print_error "Please install Python 3.8+ from: https://www.python.org/downloads/"
    exit 1
else
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    print_success "Python version: $PYTHON_VERSION"
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed!"
    print_error "Please install Node.js 16+ from: https://nodejs.org/"
    exit 1
else
    NODE_VERSION=$(node --version)
    print_success "Node.js version: $NODE_VERSION"
fi

# Check npm
if ! command -v npm &> /dev/null; then
    print_error "npm is not installed!"
    print_error "npm should come with Node.js. Please reinstall Node.js."
    exit 1
fi

# Install system dependencies
install_python_deps

# Create necessary directories
print_status "Creating project directories..."
mkdir -p uploads historical_data logs

# Setup Python virtual environment
print_status "Setting up Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    print_success "Virtual environment created!"
else
    print_status "Virtual environment already exists."
fi

# Activate virtual environment and install dependencies
print_status "Installing Python packages..."
source venv/bin/activate
pip install --upgrade pip

cd backend
pip install -r requirements.txt
touch .deps_installed
print_success "Python dependencies installed!"
cd ..

# Install Node.js dependencies
print_status "Installing Node.js packages..."
cd frontend
npm install
print_success "Node.js dependencies installed!"
cd ..

# Create environment file
if [ ! -f "backend/.env" ]; then
    print_status "Creating environment configuration..."
    cp backend/.env.example backend/.env
    print_success "Environment file created at backend/.env"
    print_warning "Please edit backend/.env with your API keys if needed."
fi

# Make scripts executable
chmod +x start.sh stop.sh install.sh

echo ""
echo "🎉 ================================="
echo "✅ INSTALLATION COMPLETED SUCCESSFULLY!"
echo "🎉 ================================="
echo ""
echo "🚀 To start the platform:"
echo "   ./start.sh"
echo ""
echo "🛑 To stop the platform:"
echo "   ./stop.sh"
echo ""
echo "⚙️  Configuration:"
echo "   • Edit backend/.env for API keys"
echo "   • Upload scripts via the web interface"
echo "   • Example scripts are in examples/ directory"
echo ""
echo "📚 Documentation:"
echo "   • README.md - Complete usage guide"
echo "   • examples/ - Sample trading strategies"
echo ""
echo "🔗 GitHub Ready:"
echo "   • All dependencies listed in requirements.txt and package.json"
echo "   • Docker support available with docker-compose.yml"
echo "   • One-command installation and startup"
echo ""
print_success "Ready to run: ./start.sh"