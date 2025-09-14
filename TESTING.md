# AI Applications Workshop - Testing Guide

This repository contains comprehensive tests for the AI Applications Workshop, including three main AI applications:

1. **AI Chatbot** - Interactive conversational agent
2. **Text Analyzer** - Text processing and sentiment analysis  
3. **Image Analyzer** - Image pattern and color analysis
4. **Web Interface** - Interactive HTML interface for all applications

## Applications Overview

### 🤖 AI Chatbot (`chatbot_app.py`)
- Responds to questions about AI, machine learning, and applications
- Maintains conversation history
- Supports custom response patterns
- Pattern-based response matching with sentiment awareness

### 📝 Text Analyzer (`text_analyzer.py`)  
- Sentiment analysis (positive, negative, neutral)
- Text statistics (word count, readability metrics)
- Word frequency analysis (excluding stop words)
- Readability scoring with grade-level estimates

### 🖼️ Image Analyzer (`image_analyzer.py`)
- Color analysis and categorization
- Brightness distribution analysis
- Pattern detection (checkerboard, stripes, uniform colors)
- Image generation for testing purposes

### 🌐 Web Interface (`index.html`)
- Interactive demos of all AI applications
- Real-time text and image analysis
- Responsive design with modern UI

## Test Coverage

Our comprehensive test suite includes:

### Unit Tests
- **97 test cases** covering all core functionality
- **79% code coverage** across all applications
- Individual component testing with mocking where appropriate
- Edge case and error condition testing

### Integration Tests  
- Cross-application workflows
- End-to-end user scenarios
- Performance and stress testing
- Web interface validation

### Test Categories
- ✅ **Input validation and sanitization**
- ✅ **Algorithm correctness** (sentiment analysis, color detection, pattern recognition)
- ✅ **Error handling and edge cases**
- ✅ **Performance with realistic data sizes**
- ✅ **Memory management and cleanup**
- ✅ **Multi-instance independence**
- ✅ **Data persistence and state management**

## Running the Tests

### Prerequisites
```bash
# Install Python 3.8+ and pip
pip install pytest pytest-cov pytest-html coverage
```

### Quick Start
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage report
python -m pytest tests/ --cov=workshop/solution --cov-report=html

# Run specific test categories
python -m pytest tests/unit/ -v          # Unit tests only
python -m pytest tests/integration/ -v   # Integration tests only

# Run with detailed output
python run_tests.py
```

### Test Configuration
Tests are configured via `pytest.ini`:
- Minimum 80% coverage requirement
- HTML and terminal coverage reports
- Automatic test discovery
- Custom markers for slow/integration tests

## Test Structure

```
tests/
├── conftest.py                 # Test configuration and fixtures
├── unit/                       # Unit tests
│   ├── test_chatbot.py        # Chatbot functionality tests
│   ├── test_text_analyzer.py  # Text analysis tests
│   └── test_image_analyzer.py # Image analysis tests
└── integration/                # Integration tests
    └── test_ai_apps_integration.py  # Cross-application tests
```

## Continuous Integration

The repository includes GitHub Actions workflows that:
- Test across Python versions 3.8-3.12
- Run linting with flake8
- Generate coverage reports
- Archive test artifacts
- Validate web interface
- Perform integration testing

## Coverage Reports

After running tests with coverage:
- **HTML Report**: `htmlcov/index.html`
- **Terminal Report**: Shows missing lines
- **XML Report**: `coverage.xml` for CI/CD

### Current Coverage
- **Chatbot**: 74% coverage
- **Text Analyzer**: 70% coverage  
- **Image Analyzer**: 85% coverage
- **Overall**: 79% coverage

## Test Examples

### Running Specific Tests
```bash
# Test just the chatbot
python -m pytest tests/unit/test_chatbot.py -v

# Test error handling across all apps
python -m pytest tests/integration/ -k "error_handling" -v

# Run with custom markers
python -m pytest tests/ -m "not slow" -v
```

### Manual Testing
```bash
# Test applications directly
cd workshop/solution
python chatbot_app.py      # Interactive chatbot
python text_analyzer.py   # Interactive text analysis
python image_analyzer.py  # Demo image analysis

# Open web interface
open index.html           # Interactive web demos
```

## Contributing

When adding new features or tests:

1. **Write tests first** (TDD approach)
2. **Maintain coverage** above 75%
3. **Test edge cases** and error conditions
4. **Update integration tests** for cross-application features
5. **Run full test suite** before committing

### Test Naming Conventions
- `test_<functionality>_<condition>` for unit tests
- `test_<workflow>_scenario` for integration tests
- Use descriptive test names and docstrings

## Performance Benchmarks

The test suite includes performance validation:
- **Chatbot**: Handles 100+ conversations efficiently
- **Text Analyzer**: Processes 1000+ word documents
- **Image Analyzer**: Analyzes 25x25 pixel images quickly
- **Memory Usage**: Stable across long-running sessions

## Troubleshooting Tests

### Common Issues
1. **Import Errors**: Ensure `workshop/solution` is in Python path
2. **Coverage Too Low**: Add tests for missing code paths
3. **Flaky Tests**: Check for randomization or timing dependencies
4. **Slow Tests**: Use `-m "not slow"` to skip performance tests

### Debug Mode
```bash
# Run with verbose output and stop on first failure
python -m pytest tests/ -v -x --tb=long

# Enable debug logging
python -m pytest tests/ --log-cli-level=DEBUG
```

## Test Data

Tests use generated and fixture data:
- **Sample texts** with known sentiment patterns
- **Generated images** with predictable characteristics  
- **Conversation flows** covering common scenarios
- **Edge cases** including empty/invalid inputs

This comprehensive test suite ensures the AI applications are robust, reliable, and ready for educational use.