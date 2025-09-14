"""
Simple Image Analysis AI Application
Performs basic image analysis including color detection, brightness analysis,
and simple pattern recognition for educational purposes.
"""

import json
import math
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter
import base64
from io import BytesIO


class ImageAnalyzer:
    """A simple image analyzer for educational AI demonstrations."""
    
    def __init__(self):
        """Initialize the image analyzer."""
        # Predefined color categories for classification
        self.color_ranges = {
            'red': [(180, 50, 50), (255, 100, 100)],
            'green': [(50, 180, 50), (100, 255, 100)],
            'blue': [(50, 50, 180), (100, 100, 255)],
            'yellow': [(180, 180, 50), (255, 255, 100)],
            'purple': [(180, 50, 180), (255, 100, 255)],
            'orange': [(255, 140, 50), (255, 200, 100)],
            'cyan': [(50, 180, 180), (100, 255, 255)],
            'white': [(200, 200, 200), (255, 255, 255)],
            'gray': [(100, 100, 100), (200, 200, 200)],
            'black': [(0, 0, 0), (50, 50, 50)]
        }
        
        self.brightness_categories = {
            'very_dark': (0, 50),
            'dark': (50, 100),
            'dim': (100, 150),
            'normal': (150, 200),
            'bright': (200, 240),
            'very_bright': (240, 255)
        }
    
    def analyze_image_data(self, image_data: List[List[List[int]]]) -> Dict[str, Any]:
        """
        Analyze image data represented as a 3D list (height x width x RGB).
        
        Args:
            image_data: 3D list representing image [height][width][rgb]
            
        Returns:
            Dict containing analysis results
        """
        if not self._validate_image_data(image_data):
            return self._empty_analysis("Invalid image data format")
        
        try:
            # Basic image properties
            height = len(image_data)
            width = len(image_data[0]) if height > 0 else 0
            total_pixels = height * width
            
            if total_pixels == 0:
                return self._empty_analysis("Image has no pixels")
            
            # Extract all pixels
            pixels = self._extract_pixels(image_data)
            
            # Color analysis
            color_analysis = self._analyze_colors(pixels)
            
            # Brightness analysis
            brightness_analysis = self._analyze_brightness(pixels)
            
            # Pattern analysis (basic)
            pattern_analysis = self._analyze_patterns(image_data)
            
            # Generate summary
            summary = self._generate_image_summary(
                height, width, color_analysis, brightness_analysis
            )
            
            return {
                'dimensions': {
                    'width': width,
                    'height': height,
                    'total_pixels': total_pixels
                },
                'colors': color_analysis,
                'brightness': brightness_analysis,
                'patterns': pattern_analysis,
                'summary': summary
            }
            
        except Exception as e:
            return self._empty_analysis(f"Error analyzing image: {str(e)}")
    
    def create_sample_image(self, width: int = 10, height: int = 10, 
                          pattern: str = 'random') -> List[List[List[int]]]:
        """
        Create a sample image for testing purposes.
        
        Args:
            width: Image width in pixels
            height: Image height in pixels  
            pattern: Pattern type ('random', 'gradient', 'checkerboard')
            
        Returns:
            3D list representing image data
        """
        import random
        
        image = []
        
        for y in range(height):
            row = []
            for x in range(width):
                if pattern == 'random':
                    pixel = [random.randint(0, 255) for _ in range(3)]
                elif pattern == 'gradient':
                    intensity = int((x / width) * 255)
                    pixel = [intensity, intensity, intensity]
                elif pattern == 'checkerboard':
                    if (x + y) % 2 == 0:
                        pixel = [255, 255, 255]  # White
                    else:
                        pixel = [0, 0, 0]  # Black
                elif pattern == 'red_square':
                    if 3 <= x < width-3 and 3 <= y < height-3:
                        pixel = [255, 0, 0]  # Red
                    else:
                        pixel = [255, 255, 255]  # White background
                else:
                    pixel = [128, 128, 128]  # Gray default
                
                row.append(pixel)
            image.append(row)
        
        return image
    
    def _validate_image_data(self, image_data: Any) -> bool:
        """Validate image data format."""
        try:
            if not isinstance(image_data, list) or len(image_data) == 0:
                return False
            
            if not isinstance(image_data[0], list) or len(image_data[0]) == 0:
                return False
            
            if not isinstance(image_data[0][0], list) or len(image_data[0][0]) != 3:
                return False
            
            # Check all pixels have RGB values
            for row in image_data:
                if not isinstance(row, list):
                    return False
                for pixel in row:
                    if not isinstance(pixel, list) or len(pixel) != 3:
                        return False
                    for value in pixel:
                        if not isinstance(value, (int, float)) or value < 0 or value > 255:
                            return False
            
            return True
        except Exception:
            return False
    
    def _extract_pixels(self, image_data: List[List[List[int]]]) -> List[Tuple[int, int, int]]:
        """Extract all pixels as RGB tuples."""
        pixels = []
        for row in image_data:
            for pixel in row:
                pixels.append((int(pixel[0]), int(pixel[1]), int(pixel[2])))
        return pixels
    
    def _analyze_colors(self, pixels: List[Tuple[int, int, int]]) -> Dict[str, Any]:
        """Analyze color distribution in the image."""
        if not pixels:
            return {'dominant_colors': [], 'color_categories': {}, 'color_diversity': 0}
        
        # Count unique colors
        color_counts = Counter(pixels)
        total_pixels = len(pixels)
        
        # Get dominant colors (top 5)
        dominant_colors = []
        for (r, g, b), count in color_counts.most_common(5):
            dominant_colors.append({
                'rgb': [r, g, b],
                'hex': f'#{r:02x}{g:02x}{b:02x}',
                'count': count,
                'percentage': round((count / total_pixels) * 100, 2)
            })
        
        # Categorize colors
        color_categories = {}
        for color_name in self.color_ranges:
            color_categories[color_name] = 0
        
        for r, g, b in pixels:
            category = self._categorize_color(r, g, b)
            color_categories[category] += 1
        
        # Convert to percentages
        for color_name in color_categories:
            color_categories[color_name] = round(
                (color_categories[color_name] / total_pixels) * 100, 1
            )
        
        # Calculate color diversity (number of unique colors / total pixels)
        color_diversity = round(len(color_counts) / total_pixels, 3)
        
        return {
            'dominant_colors': dominant_colors,
            'color_categories': color_categories,
            'color_diversity': color_diversity,
            'unique_colors': len(color_counts)
        }
    
    def _categorize_color(self, r: int, g: int, b: int) -> str:
        """Categorize an RGB color into a named color category."""
        for color_name, (min_rgb, max_rgb) in self.color_ranges.items():
            if (min_rgb[0] <= r <= max_rgb[0] and 
                min_rgb[1] <= g <= max_rgb[1] and 
                min_rgb[2] <= b <= max_rgb[2]):
                return color_name
        
        # If no category matches, classify by brightness
        brightness = (r + g + b) / 3
        if brightness < 85:
            return 'black'
        elif brightness > 170:
            return 'white'
        else:
            return 'gray'
    
    def _analyze_brightness(self, pixels: List[Tuple[int, int, int]]) -> Dict[str, Any]:
        """Analyze brightness distribution in the image."""
        if not pixels:
            return {'average': 0, 'distribution': {}, 'category': 'unknown'}
        
        # Calculate brightness for each pixel (using luminance formula)
        brightness_values = []
        for r, g, b in pixels:
            # Standard luminance calculation
            brightness = 0.299 * r + 0.587 * g + 0.114 * b
            brightness_values.append(brightness)
        
        # Calculate statistics
        avg_brightness = sum(brightness_values) / len(brightness_values)
        min_brightness = min(brightness_values)
        max_brightness = max(brightness_values)
        
        # Categorize brightness distribution
        distribution = {}
        for category, (min_val, max_val) in self.brightness_categories.items():
            count = sum(1 for b in brightness_values if min_val <= b < max_val)
            distribution[category] = round((count / len(brightness_values)) * 100, 1)
        
        # Determine overall brightness category
        overall_category = self._categorize_brightness(avg_brightness)
        
        return {
            'average': round(avg_brightness, 1),
            'min': round(min_brightness, 1),
            'max': round(max_brightness, 1),
            'distribution': distribution,
            'category': overall_category
        }
    
    def _categorize_brightness(self, brightness: float) -> str:
        """Categorize overall brightness value."""
        for category, (min_val, max_val) in self.brightness_categories.items():
            if min_val <= brightness < max_val:
                return category
        return 'very_bright'  # fallback
    
    def _analyze_patterns(self, image_data: List[List[List[int]]]) -> Dict[str, Any]:
        """Perform basic pattern analysis."""
        if not image_data or not image_data[0]:
            return {'detected_patterns': [], 'uniformity': 0}
        
        height = len(image_data)
        width = len(image_data[0])
        patterns = []
        
        # Check for uniform color
        first_pixel = image_data[0][0]
        is_uniform = True
        for row in image_data:
            for pixel in row:
                if pixel != first_pixel:
                    is_uniform = False
                    break
            if not is_uniform:
                break
        
        if is_uniform:
            patterns.append("uniform_color")
        
        # Check for horizontal stripes
        has_horizontal_stripes = self._detect_horizontal_stripes(image_data)
        if has_horizontal_stripes:
            patterns.append("horizontal_stripes")
        
        # Check for vertical stripes
        has_vertical_stripes = self._detect_vertical_stripes(image_data)
        if has_vertical_stripes:
            patterns.append("vertical_stripes")
        
        # Check for checkerboard pattern (basic)
        has_checkerboard = self._detect_checkerboard(image_data)
        if has_checkerboard:
            patterns.append("checkerboard")
        
        # Calculate uniformity score (similarity between adjacent pixels)
        uniformity = self._calculate_uniformity(image_data)
        
        return {
            'detected_patterns': patterns,
            'uniformity': round(uniformity, 3),
            'pattern_count': len(patterns)
        }
    
    def _detect_horizontal_stripes(self, image_data: List[List[List[int]]]) -> bool:
        """Detect horizontal stripe patterns."""
        if len(image_data) < 2:
            return False
        
        # Check if alternate rows are similar
        stripe_detected = True
        for i in range(0, len(image_data) - 2, 2):
            if not self._rows_similar(image_data[i], image_data[i + 2]):
                stripe_detected = False
                break
        
        return stripe_detected and len(image_data) >= 4
    
    def _detect_vertical_stripes(self, image_data: List[List[List[int]]]) -> bool:
        """Detect vertical stripe patterns."""
        if not image_data or len(image_data[0]) < 2:
            return False
        
        # Check if alternate columns are similar
        height = len(image_data)
        width = len(image_data[0])
        
        if width < 4:
            return False
        
        for col in range(0, width - 2, 2):
            col1_pixels = [image_data[row][col] for row in range(height)]
            col2_pixels = [image_data[row][col + 2] for row in range(height)]
            
            if not self._pixel_lists_similar(col1_pixels, col2_pixels):
                return False
        
        return True
    
    def _detect_checkerboard(self, image_data: List[List[List[int]]]) -> bool:
        """Detect checkerboard patterns."""
        if len(image_data) < 2 or len(image_data[0]) < 2:
            return False
        
        # Sample a few positions to check alternating pattern
        height = len(image_data)
        width = len(image_data[0])
        
        # Check if pixels alternate in checkerboard pattern
        sample_positions = [
            (0, 0), (0, 1), (1, 0), (1, 1)
        ]
        
        if height < 2 or width < 2:
            return False
        
        # Get colors at key positions
        tl = image_data[0][0]  # top-left
        tr = image_data[0][1]  # top-right
        bl = image_data[1][0]  # bottom-left
        br = image_data[1][1]  # bottom-right
        
        # In checkerboard, diagonals should be same color
        return (self._pixels_similar(tl, br) and 
                self._pixels_similar(tr, bl) and 
                not self._pixels_similar(tl, tr))
    
    def _rows_similar(self, row1: List[List[int]], row2: List[List[int]], 
                     threshold: int = 30) -> bool:
        """Check if two rows are similar."""
        if len(row1) != len(row2):
            return False
        
        differences = 0
        for p1, p2 in zip(row1, row2):
            if not self._pixels_similar(p1, p2, threshold):
                differences += 1
        
        # Allow up to 20% different pixels
        return differences / len(row1) <= 0.2
    
    def _pixel_lists_similar(self, list1: List[List[int]], list2: List[List[int]], 
                           threshold: int = 30) -> bool:
        """Check if two lists of pixels are similar."""
        if len(list1) != len(list2):
            return False
        
        differences = 0
        for p1, p2 in zip(list1, list2):
            if not self._pixels_similar(p1, p2, threshold):
                differences += 1
        
        return differences / len(list1) <= 0.2
    
    def _pixels_similar(self, pixel1: List[int], pixel2: List[int], 
                       threshold: int = 30) -> bool:
        """Check if two pixels are similar within threshold."""
        diff = sum(abs(pixel1[i] - pixel2[i]) for i in range(3))
        return diff <= threshold
    
    def _calculate_uniformity(self, image_data: List[List[List[int]]]) -> float:
        """Calculate uniformity score of the image."""
        if not image_data or not image_data[0]:
            return 0
        
        height = len(image_data)
        width = len(image_data[0])
        total_comparisons = 0
        similar_pairs = 0
        
        # Compare adjacent pixels
        for y in range(height):
            for x in range(width):
                current = image_data[y][x]
                
                # Check right neighbor
                if x < width - 1:
                    right = image_data[y][x + 1]
                    total_comparisons += 1
                    if self._pixels_similar(current, right):
                        similar_pairs += 1
                
                # Check bottom neighbor
                if y < height - 1:
                    bottom = image_data[y + 1][x]
                    total_comparisons += 1
                    if self._pixels_similar(current, bottom):
                        similar_pairs += 1
        
        return similar_pairs / total_comparisons if total_comparisons > 0 else 0
    
    def _generate_image_summary(self, height: int, width: int, 
                              color_analysis: Dict, brightness_analysis: Dict) -> str:
        """Generate human-readable summary of image analysis."""
        summary_parts = []
        
        # Size description
        total_pixels = height * width
        if total_pixels < 100:
            summary_parts.append("This is a very small image")
        elif total_pixels < 1000:
            summary_parts.append("This is a small image")
        elif total_pixels < 10000:
            summary_parts.append("This is a medium-sized image")
        else:
            summary_parts.append("This is a large image")
        
        summary_parts.append(f"({width}x{height} pixels)")
        
        # Dominant colors
        if color_analysis['dominant_colors']:
            dominant = color_analysis['dominant_colors'][0]
            summary_parts.append(f"with {dominant['rgb']} as the dominant color")
        
        # Brightness
        brightness_cat = brightness_analysis['category'].replace('_', ' ')
        summary_parts.append(f"The image is {brightness_cat}")
        
        # Color diversity
        diversity = color_analysis['color_diversity']
        if diversity > 0.5:
            summary_parts.append("and has high color diversity")
        elif diversity > 0.1:
            summary_parts.append("and has moderate color diversity")
        else:
            summary_parts.append("and has low color diversity")
        
        return " ".join(summary_parts) + "."
    
    def _empty_analysis(self, reason: str = "No image data") -> Dict[str, Any]:
        """Return empty analysis with error reason."""
        return {
            'error': reason,
            'dimensions': {'width': 0, 'height': 0, 'total_pixels': 0},
            'colors': {'dominant_colors': [], 'color_categories': {}, 'color_diversity': 0, 'unique_colors': 0},
            'brightness': {'average': 0, 'distribution': {}, 'category': 'unknown'},
            'patterns': {'detected_patterns': [], 'uniformity': 0},
            'summary': reason
        }


def main():
    """Main function to demonstrate image analysis."""
    analyzer = ImageAnalyzer()
    
    print("🖼️ Image Analyzer AI initialized!")
    print("Analyzing sample images...\n")
    
    # Create and analyze different sample images
    test_cases = [
        ('Random Colors (10x10)', 'random'),
        ('Gradient (10x10)', 'gradient'),
        ('Checkerboard (8x8)', 'checkerboard'),
        ('Red Square (12x12)', 'red_square')
    ]
    
    for name, pattern in test_cases:
        print(f"Analyzing: {name}")
        print("-" * 40)
        
        # Create sample image
        if 'checkerboard' in pattern:
            image = analyzer.create_sample_image(8, 8, pattern)
        elif 'red_square' in pattern:
            image = analyzer.create_sample_image(12, 12, pattern)
        else:
            image = analyzer.create_sample_image(10, 10, pattern)
        
        # Analyze image
        analysis = analyzer.analyze_image_data(image)
        
        # Display results
        if 'error' not in analysis:
            dims = analysis['dimensions']
            colors = analysis['colors']
            brightness = analysis['brightness']
            patterns = analysis['patterns']
            
            print(f"📏 Size: {dims['width']}x{dims['height']} ({dims['total_pixels']} pixels)")
            print(f"🎨 Unique colors: {colors['unique_colors']}")
            print(f"💡 Average brightness: {brightness['average']} ({brightness['category']})")
            print(f"🔍 Patterns detected: {', '.join(patterns['detected_patterns']) if patterns['detected_patterns'] else 'None'}")
            print(f"📝 Summary: {analysis['summary']}")
        else:
            print(f"❌ Error: {analysis['error']}")
        
        print("\n")
    
    print("Demo complete! This analyzer can process image data represented as 3D lists.")


if __name__ == "__main__":
    main()