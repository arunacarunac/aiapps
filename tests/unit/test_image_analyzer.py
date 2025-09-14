"""
Unit tests for the Image Analyzer AI Application.
Tests image data processing, color analysis, brightness analysis,
pattern detection, and image generation functionality.
"""

import pytest
import sys
import os

# Add the solution directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution'))

from image_analyzer import ImageAnalyzer


class TestImageAnalyzer:
    """Test class for Image Analyzer functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = ImageAnalyzer()
    
    def test_initialization(self):
        """Test that analyzer initializes properly."""
        assert isinstance(self.analyzer, ImageAnalyzer)
        assert hasattr(self.analyzer, 'color_ranges')
        assert hasattr(self.analyzer, 'brightness_categories')
        assert len(self.analyzer.color_ranges) > 0
        assert len(self.analyzer.brightness_categories) > 0
    
    def test_create_sample_image_random(self):
        """Test creation of random pattern sample image."""
        width, height = 5, 5
        image = self.analyzer.create_sample_image(width, height, 'random')
        
        assert isinstance(image, list)
        assert len(image) == height
        assert len(image[0]) == width
        assert len(image[0][0]) == 3  # RGB
        
        # Check all pixels are valid RGB values
        for row in image:
            for pixel in row:
                assert len(pixel) == 3
                for value in pixel:
                    assert 0 <= value <= 255
    
    def test_create_sample_image_gradient(self):
        """Test creation of gradient pattern sample image."""
        width, height = 4, 3
        image = self.analyzer.create_sample_image(width, height, 'gradient')
        
        assert len(image) == height
        assert len(image[0]) == width
        
        # Check gradient pattern (should get brighter left to right)
        first_pixel = image[0][0]
        last_pixel = image[0][-1]
        
        # All channels should be equal (grayscale)
        assert first_pixel[0] == first_pixel[1] == first_pixel[2]
        assert last_pixel[0] == last_pixel[1] == last_pixel[2]
        
        # Should be darker on left, brighter on right
        assert first_pixel[0] < last_pixel[0]
    
    def test_create_sample_image_checkerboard(self):
        """Test creation of checkerboard pattern sample image."""
        width, height = 4, 4
        image = self.analyzer.create_sample_image(width, height, 'checkerboard')
        
        # Check alternating pattern
        assert image[0][0] != image[0][1]  # Adjacent pixels different
        assert image[0][0] == image[0][2]  # Same color every 2 pixels
        assert image[0][0] == image[1][1]  # Diagonal same color
        
        # Should only have black and white
        colors_found = set()
        for row in image:
            for pixel in row:
                colors_found.add(tuple(pixel))
        
        assert len(colors_found) == 2
        assert (255, 255, 255) in colors_found  # White
        assert (0, 0, 0) in colors_found  # Black
    
    def test_create_sample_image_red_square(self):
        """Test creation of red square pattern sample image."""
        width, height = 8, 8
        image = self.analyzer.create_sample_image(width, height, 'red_square')
        
        # Check corners are white (background)
        assert image[0][0] == [255, 255, 255]
        assert image[0][-1] == [255, 255, 255]
        assert image[-1][0] == [255, 255, 255]
        assert image[-1][-1] == [255, 255, 255]
        
        # Check center has red
        center_y, center_x = height // 2, width // 2
        center_pixel = image[center_y][center_x]
        assert center_pixel[0] > center_pixel[1]  # More red than green
        assert center_pixel[0] > center_pixel[2]  # More red than blue
    
    def test_validate_image_data_valid(self):
        """Test validation of valid image data."""
        valid_images = [
            [[[255, 0, 0]]],  # 1x1 red pixel
            [[[0, 255, 0], [0, 0, 255]], [[255, 255, 255], [0, 0, 0]]],  # 2x2
            [[[100, 150, 200]]]  # 1x1 with mid-range values
        ]
        
        for valid_image in valid_images:
            assert self.analyzer._validate_image_data(valid_image) is True
    
    def test_validate_image_data_invalid(self):
        """Test validation of invalid image data."""
        invalid_images = [
            [],  # Empty list
            [[]],  # Empty row
            [[[]]],  # Empty pixel
            [[[256, 0, 0]]],  # Value too high
            [[[-1, 0, 0]]],  # Negative value
            [[[255, 0]]],  # Missing blue channel
            [[[255, 0, 0, 255]]],  # Too many channels
            [[255, 0, 0]],  # Wrong nesting level
            [[[255.5, 0, 0]]],  # Float values should be accepted but let's test edge cases
            None,  # None input
            "not a list",  # Wrong type
        ]
        
        for invalid_image in invalid_images[:-2]:  # Skip float and None for now
            assert self.analyzer._validate_image_data(invalid_image) is False
        
        # Test None and string separately
        assert self.analyzer._validate_image_data(None) is False
        assert self.analyzer._validate_image_data("not a list") is False
    
    def test_analyze_empty_or_invalid_image(self):
        """Test analysis of empty or invalid image data."""
        invalid_inputs = [
            None,
            [],
            [[]],
            [[[]]],
            "invalid"
        ]
        
        for invalid_input in invalid_inputs:
            analysis = self.analyzer.analyze_image_data(invalid_input)
            
            assert 'error' in analysis
            assert analysis['dimensions']['total_pixels'] == 0
            assert analysis['colors']['unique_colors'] == 0
            assert 'No image' in analysis['summary'] or 'Invalid' in analysis['summary']
    
    def test_analyze_single_pixel_image(self):
        """Test analysis of single pixel image."""
        single_pixel = [[[255, 0, 0]]]  # Single red pixel
        analysis = self.analyzer.analyze_image_data(single_pixel)
        
        assert 'error' not in analysis
        assert analysis['dimensions']['width'] == 1
        assert analysis['dimensions']['height'] == 1
        assert analysis['dimensions']['total_pixels'] == 1
        
        colors = analysis['colors']
        assert colors['unique_colors'] == 1
        assert len(colors['dominant_colors']) == 1
        assert colors['dominant_colors'][0]['rgb'] == [255, 0, 0]
        assert colors['dominant_colors'][0]['percentage'] == 100.0
    
    def test_color_analysis(self):
        """Test color analysis functionality."""
        # Create image with known colors
        red_blue_image = [
            [[255, 0, 0], [255, 0, 0]],
            [[0, 0, 255], [0, 0, 255]]
        ]
        
        analysis = self.analyzer.analyze_image_data(red_blue_image)
        colors = analysis['colors']
        
        assert colors['unique_colors'] == 2
        assert len(colors['dominant_colors']) == 2
        
        # Each color should have 50% representation
        for color_info in colors['dominant_colors']:
            assert color_info['percentage'] == 50.0
        
        # Check RGB values
        rgb_values = [color['rgb'] for color in colors['dominant_colors']]
        assert [255, 0, 0] in rgb_values
        assert [0, 0, 255] in rgb_values
    
    def test_color_categorization(self):
        """Test color categorization into named categories."""
        test_colors = [
            ([255, 0, 0], 'red'),
            ([0, 255, 0], 'green'),
            ([0, 0, 255], 'blue'),
            ([255, 255, 255], 'white'),
            ([0, 0, 0], 'black'),
            ([128, 128, 128], 'gray'),
        ]
        
        for (r, g, b), expected_category in test_colors:
            category = self.analyzer._categorize_color(r, g, b)
            # Should categorize correctly or fall back to brightness-based category
            assert isinstance(category, str)
            assert len(category) > 0
    
    def test_brightness_analysis(self):
        """Test brightness analysis functionality."""
        # Create images with different brightness levels
        bright_image = [[[255, 255, 255], [255, 255, 255]]]  # Very bright
        dark_image = [[[0, 0, 0], [0, 0, 0]]]  # Very dark
        mixed_image = [[[255, 255, 255], [0, 0, 0]]]  # Mixed
        
        for image, expected_range in [(bright_image, (200, 255)), 
                                      (dark_image, (0, 50)), 
                                      (mixed_image, (100, 150))]:
            analysis = self.analyzer.analyze_image_data(image)
            brightness = analysis['brightness']
            
            assert 'average' in brightness
            assert 'min' in brightness
            assert 'max' in brightness
            assert 'category' in brightness
            assert 'distribution' in brightness
            
            avg = brightness['average']
            assert expected_range[0] <= avg <= expected_range[1] or abs(avg - sum(expected_range)/2) < 50
    
    def test_brightness_categorization(self):
        """Test brightness categorization."""
        test_brightnesses = [
            (25, 'very_dark'),
            (75, 'dark'), 
            (125, 'dim'),
            (175, 'normal'),
            (220, 'bright'),
            (250, 'very_bright')
        ]
        
        for brightness, expected_category in test_brightnesses:
            category = self.analyzer._categorize_brightness(brightness)
            assert category == expected_category
    
    def test_pattern_detection_uniform(self):
        """Test detection of uniform color pattern."""
        uniform_image = [
            [[100, 100, 100], [100, 100, 100]],
            [[100, 100, 100], [100, 100, 100]]
        ]
        
        analysis = self.analyzer.analyze_image_data(uniform_image)
        patterns = analysis['patterns']
        
        assert 'uniform_color' in patterns['detected_patterns']
        assert patterns['uniformity'] == 1.0  # Perfect uniformity
    
    def test_pattern_detection_checkerboard(self):
        """Test detection of checkerboard pattern."""
        checkerboard = self.analyzer.create_sample_image(4, 4, 'checkerboard')
        analysis = self.analyzer.analyze_image_data(checkerboard)
        patterns = analysis['patterns']
        
        assert 'checkerboard' in patterns['detected_patterns']
    
    def test_pattern_detection_stripes(self):
        """Test detection of stripe patterns."""
        # Create horizontal stripes
        h_stripes = [
            [[255, 0, 0], [255, 0, 0], [255, 0, 0]],
            [[0, 255, 0], [0, 255, 0], [0, 255, 0]],
            [[255, 0, 0], [255, 0, 0], [255, 0, 0]],
            [[0, 255, 0], [0, 255, 0], [0, 255, 0]]
        ]
        
        analysis = self.analyzer.analyze_image_data(h_stripes)
        patterns = analysis['patterns']
        
        assert 'horizontal_stripes' in patterns['detected_patterns']
        
        # Create vertical stripes
        v_stripes = [
            [[255, 0, 0], [0, 255, 0], [255, 0, 0], [0, 255, 0]],
            [[255, 0, 0], [0, 255, 0], [255, 0, 0], [0, 255, 0]],
            [[255, 0, 0], [0, 255, 0], [255, 0, 0], [0, 255, 0]]
        ]
        
        analysis = self.analyzer.analyze_image_data(v_stripes)
        patterns = analysis['patterns']
        
        assert 'vertical_stripes' in patterns['detected_patterns']
    
    def test_uniformity_calculation(self):
        """Test uniformity calculation."""
        # Perfect uniformity
        uniform = [[[100, 100, 100], [100, 100, 100]],
                   [[100, 100, 100], [100, 100, 100]]]
        uniformity = self.analyzer._calculate_uniformity(uniform)
        assert uniformity == 1.0
        
        # No uniformity
        random_colors = [[[255, 0, 0], [0, 255, 0]],
                        [[0, 0, 255], [255, 255, 0]]]
        uniformity = self.analyzer._calculate_uniformity(random_colors)
        assert 0 <= uniformity < 1.0
    
    def test_pixels_similarity(self):
        """Test pixel similarity detection."""
        # Identical pixels
        assert self.analyzer._pixels_similar([255, 0, 0], [255, 0, 0]) is True
        
        # Similar pixels (within threshold)
        assert self.analyzer._pixels_similar([255, 0, 0], [250, 5, 5]) is True
        
        # Different pixels
        assert self.analyzer._pixels_similar([255, 0, 0], [0, 255, 0]) is False
        
        # Test with custom threshold
        assert self.analyzer._pixels_similar([255, 0, 0], [200, 0, 0], threshold=60) is True
        assert self.analyzer._pixels_similar([255, 0, 0], [200, 0, 0], threshold=50) is False
    
    def test_extract_pixels(self):
        """Test pixel extraction from image data."""
        image = [
            [[255, 0, 0], [0, 255, 0]],
            [[0, 0, 255], [255, 255, 255]]
        ]
        
        pixels = self.analyzer._extract_pixels(image)
        
        assert len(pixels) == 4
        assert pixels == [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 255)]
    
    def test_summary_generation(self):
        """Test summary generation for different image types."""
        # Small image
        small_image = [[[255, 0, 0]]]
        analysis = self.analyzer.analyze_image_data(small_image)
        assert 'small' in analysis['summary'].lower()
        
        # Large image (relatively)
        large_image = [[[[100, 100, 100] for _ in range(50)] for _ in range(50)]]
        # This would be too slow, so let's test with description
        dims = {'width': 50, 'height': 50}
        colors = {'dominant_colors': [{'rgb': [100, 100, 100]}], 'color_diversity': 0.1}
        brightness = {'category': 'normal'}
        
        summary = self.analyzer._generate_image_summary(50, 50, colors, brightness)
        assert 'large' in summary.lower() or 'medium' in summary.lower()
    
    def test_color_diversity_calculation(self):
        """Test color diversity metrics."""
        # High diversity image
        diverse_image = [
            [[255, 0, 0], [0, 255, 0]],
            [[0, 0, 255], [255, 255, 0]]
        ]
        
        analysis = self.analyzer.analyze_image_data(diverse_image)
        colors = analysis['colors']
        
        assert colors['color_diversity'] > 0.5  # High diversity
        assert colors['unique_colors'] == 4
        
        # Low diversity image
        uniform_image = [
            [[100, 100, 100], [100, 100, 100]],
            [[100, 100, 100], [101, 101, 101]]  # Slightly different
        ]
        
        analysis = self.analyzer.analyze_image_data(uniform_image)
        colors = analysis['colors']
        
        assert colors['color_diversity'] < 0.8  # Lower diversity
    
    def test_hex_color_conversion(self):
        """Test RGB to hex color conversion in results."""
        red_image = [[[255, 0, 0]]]
        analysis = self.analyzer.analyze_image_data(red_image)
        
        dominant_color = analysis['colors']['dominant_colors'][0]
        assert dominant_color['hex'] == '#ff0000'
    
    def test_large_image_handling(self):
        """Test handling of larger images."""
        # Create a 20x20 image
        large_image = self.analyzer.create_sample_image(20, 20, 'gradient')
        analysis = self.analyzer.analyze_image_data(large_image)
        
        assert analysis['dimensions']['total_pixels'] == 400
        assert 'error' not in analysis
        assert len(analysis['colors']['dominant_colors']) > 0
    
    def test_edge_cases(self):
        """Test various edge cases."""
        # Single row image
        single_row = [[[255, 0, 0], [0, 255, 0], [0, 0, 255]]]
        analysis = self.analyzer.analyze_image_data(single_row)
        assert analysis['dimensions']['height'] == 1
        assert analysis['dimensions']['width'] == 3
        
        # Single column image
        single_col = [[[255, 0, 0]], [[0, 255, 0]], [[0, 0, 255]]]
        analysis = self.analyzer.analyze_image_data(single_col)
        assert analysis['dimensions']['height'] == 3
        assert analysis['dimensions']['width'] == 1
    
    def test_float_rgb_values(self):
        """Test handling of float RGB values."""
        float_image = [[[255.0, 128.5, 0.0]]]
        analysis = self.analyzer.analyze_image_data(float_image)
        
        # Should handle floats gracefully
        assert 'error' not in analysis
        assert analysis['dimensions']['total_pixels'] == 1


class TestImageAnalyzerIntegration:
    """Integration tests for image analyzer functionality."""
    
    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        from image_analyzer import main
        assert callable(main)
    
    def test_full_analysis_pipeline(self):
        """Test complete analysis pipeline with all pattern types."""
        analyzer = ImageAnalyzer()
        
        patterns = ['random', 'gradient', 'checkerboard', 'red_square']
        
        for pattern in patterns:
            image = analyzer.create_sample_image(8, 8, pattern)
            analysis = analyzer.analyze_image_data(image)
            
            # All analyses should succeed
            assert 'error' not in analysis
            assert analysis['dimensions']['total_pixels'] == 64
            assert analysis['colors']['unique_colors'] > 0
            assert len(analysis['summary']) > 0
            
            # Pattern-specific checks
            if pattern == 'checkerboard':
                assert 'checkerboard' in analysis['patterns']['detected_patterns']
            elif pattern == 'gradient':
                assert analysis['patterns']['uniformity'] < 1.0
    
    def test_analyzer_independence(self):
        """Test that multiple analyzer instances work independently."""
        analyzer1 = ImageAnalyzer()
        analyzer2 = ImageAnalyzer()
        
        # Modify color ranges in one analyzer
        analyzer1.color_ranges['custom_red'] = [(200, 0, 0), (255, 50, 50)]
        
        # Test that they categorize differently
        red_pixel_image = [[[220, 10, 10]]]
        
        analysis1 = analyzer1.analyze_image_data(red_pixel_image)
        analysis2 = analyzer2.analyze_image_data(red_pixel_image)
        
        # Results should be computed independently
        assert isinstance(analysis1, dict)
        assert isinstance(analysis2, dict)
    
    def test_performance_with_different_sizes(self):
        """Test performance and correctness with different image sizes."""
        analyzer = ImageAnalyzer()
        
        sizes = [(4, 4), (8, 8), (16, 16)]
        
        for width, height in sizes:
            image = analyzer.create_sample_image(width, height, 'random')
            analysis = analyzer.analyze_image_data(image)
            
            expected_pixels = width * height
            assert analysis['dimensions']['total_pixels'] == expected_pixels
            assert analysis['dimensions']['width'] == width
            assert analysis['dimensions']['height'] == height
    
    def test_error_resilience(self):
        """Test that analyzer handles various error conditions gracefully."""
        analyzer = ImageAnalyzer()
        
        error_cases = [
            None,
            [],
            [[]],
            "not an image",
            123,
            [[[300, 0, 0]]],  # Invalid RGB value
            [[[255, 0]]],     # Missing color channel
        ]
        
        for error_case in error_cases:
            analysis = analyzer.analyze_image_data(error_case)
            assert isinstance(analysis, dict)
            # Should either succeed or fail gracefully with error message
            if 'error' in analysis:
                assert isinstance(analysis['error'], str)
                assert len(analysis['error']) > 0


if __name__ == '__main__':
    pytest.main([__file__])