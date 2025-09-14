"""
Test configuration and fixtures for AI Applications.
"""

import pytest
import sys
import os

# Add the solution directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'workshop', 'solution'))


@pytest.fixture
def sample_chatbot():
    """Fixture providing a clean chatbot instance."""
    from chatbot_app import AIchatbot
    return AIchatbot()


@pytest.fixture
def sample_text_analyzer():
    """Fixture providing a clean text analyzer instance."""
    from text_analyzer import TextAnalyzer
    return TextAnalyzer()


@pytest.fixture
def sample_image_analyzer():
    """Fixture providing a clean image analyzer instance."""
    from image_analyzer import ImageAnalyzer
    return ImageAnalyzer()


@pytest.fixture
def sample_texts():
    """Fixture providing various sample texts for testing."""
    return {
        'positive': "This is amazing and wonderful! I love this fantastic experience.",
        'negative': "This is terrible and awful. I hate this horrible experience.",
        'neutral': "The weather report indicates partly cloudy conditions today.",
        'mixed': "Good features but bad usability. Love the design, hate the interface.",
        'short': "Hi!",
        'long': " ".join(["This is a longer text sample."] * 50),
        'empty': "",
        'whitespace': "   \t\n   "
    }


@pytest.fixture
def sample_images():
    """Fixture providing various sample images for testing."""
    from image_analyzer import ImageAnalyzer
    analyzer = ImageAnalyzer()
    
    return {
        'red_pixel': [[[255, 0, 0]]],
        'small_checkerboard': analyzer.create_sample_image(4, 4, 'checkerboard'),
        'gradient': analyzer.create_sample_image(8, 8, 'gradient'),
        'random': analyzer.create_sample_image(6, 6, 'random'),
        'red_square': analyzer.create_sample_image(10, 10, 'red_square'),
        'uniform': [[[100, 100, 100], [100, 100, 100]], 
                   [[100, 100, 100], [100, 100, 100]]]
    }


@pytest.fixture(scope="session")
def test_data_dir():
    """Fixture providing path to test data directory."""
    return os.path.join(os.path.dirname(__file__), 'data')


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )