# Contributing to Algorithmic Trading Platform

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🚀 Quick Start for Contributors

1. **Fork the repository**
2. **Clone your fork:**
   ```bash
   git clone https://github.com/your-username/algo-trading-app.git
   cd algo-trading-app
   ```
3. **Install dependencies:**
   ```bash
   ./install.sh
   ```
4. **Start development servers:**
   ```bash
   ./start.sh
   ```

## 📋 Development Guidelines

### Code Style
- **Python**: Follow PEP 8 guidelines
- **JavaScript/React**: Use ESLint configuration provided
- **Commit Messages**: Use conventional commits format

### Project Structure
```
algo-trading-app/
├── backend/           # Flask API server
├── frontend/          # React application
├── examples/          # Sample trading scripts
├── uploads/           # User uploaded scripts
├── historical_data/   # Market data cache
├── logs/             # Application logs
└── docs/             # Documentation
```

### Adding New Features

#### Backend (Flask)
1. Add new routes in `backend/app.py`
2. Update database models if needed
3. Add appropriate error handling
4. Update API documentation

#### Frontend (React)
1. Create components in `frontend/src/components/`
2. Update main App.js if adding new tabs
3. Follow Material-UI design patterns
4. Add proper error handling and loading states

#### Trading Scripts
1. Place example scripts in `examples/`
2. Follow the template format
3. Include proper documentation
4. Test with backtesting module

### Testing
- Test all new features thoroughly
- Ensure both backend and frontend work together
- Test script upload and execution
- Verify API integrations

### Submitting Changes

1. **Create a new branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes and commit:**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```

3. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**

## 🐛 Bug Reports

When reporting bugs, please include:
- Operating system and version
- Python and Node.js versions
- Steps to reproduce
- Expected vs actual behavior
- Console/log output if available

## 💡 Feature Requests

For new features:
- Explain the use case
- Describe the proposed solution
- Consider backward compatibility
- Discuss potential alternatives

## 🔒 Security Issues

For security vulnerabilities:
- Do NOT create public issues
- Email the maintainers directly
- Provide detailed reproduction steps
- Allow time for fix before disclosure

## 📚 Documentation

Help improve documentation:
- Fix typos and unclear explanations
- Add examples and use cases
- Update setup instructions
- Improve code comments

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributor graphs

Thank you for helping make this project better!