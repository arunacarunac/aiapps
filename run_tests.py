#!/usr/bin/env python3
"""
Test runner script for AI Applications.
Runs all tests and generates coverage reports.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def setup_test_environment():
    """Set up the test environment."""
    # Ensure test directories exist
    test_dirs = ['test-reports', 'htmlcov']
    for directory in test_dirs:
        Path(directory).mkdir(exist_ok=True)
    
    # Install test dependencies if needed
    try:
        import pytest
        import coverage
    except ImportError:
        print("Installing test dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements-test.txt'], 
                      check=True)


def run_tests():
    """Run all tests with coverage."""
    print("🚀 Starting AI Applications Test Suite...")
    print("=" * 50)
    
    # Run pytest with coverage
    cmd = [
        sys.executable, '-m', 'pytest',
        'tests/',
        '-v',
        '--tb=short',
        '--cov=workshop/solution',
        '--cov-report=html:htmlcov',
        '--cov-report=term-missing',
        '--cov-report=xml:coverage.xml',
        '--html=test-reports/report.html',
        '--self-contained-html',
        '--junitxml=test-reports/junit.xml'
    ]
    
    try:
        result = subprocess.run(cmd, check=False, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def run_linting():
    """Run code linting checks."""
    print("\n🔍 Running code quality checks...")
    
    # Check if flake8 is available
    try:
        subprocess.run([sys.executable, '-m', 'flake8', '--version'], 
                      check=True, capture_output=True)
        
        # Run flake8 on solution code
        result = subprocess.run([
            sys.executable, '-m', 'flake8', 
            'workshop/solution/',
            '--max-line-length=120',
            '--ignore=E501,W503'  # Ignore line too long and line break before binary operator
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Linting passed!")
        else:
            print("⚠️  Linting issues found:")
            print(result.stdout)
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Flake8 not available, skipping linting")


def generate_summary():
    """Generate a test summary."""
    print("\n📊 Test Summary")
    print("=" * 30)
    
    # Check if coverage report exists
    coverage_file = Path('htmlcov/index.html')
    if coverage_file.exists():
        print(f"📈 Coverage report: {coverage_file.absolute()}")
    
    # Check if HTML report exists
    html_report = Path('test-reports/report.html')
    if html_report.exists():
        print(f"📋 HTML test report: {html_report.absolute()}")
    
    print("\nTest files:")
    for test_file in Path('tests').rglob('test_*.py'):
        print(f"  - {test_file}")


def main():
    """Main test runner function."""
    # Change to the repository root
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("🤖 AI Applications Test Runner")
    print("=" * 50)
    
    # Setup
    setup_test_environment()
    
    # Run tests
    test_success = run_tests()
    
    # Run linting
    run_linting()
    
    # Generate summary
    generate_summary()
    
    # Final result
    print("\n" + "=" * 50)
    if test_success:
        print("✅ All tests completed successfully!")
        exit_code = 0
    else:
        print("❌ Some tests failed. Check the reports for details.")
        exit_code = 1
    
    print("=" * 50)
    return exit_code


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)