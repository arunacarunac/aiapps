"""
Integration tests for all AI Applications.
Tests how the applications work together, end-to-end functionality,
and real-world usage scenarios.
"""

import pytest
import sys
import os
import json
from unittest.mock import patch, MagicMock

# Add the solution directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution'))

from chatbot_app import AIchatbot
from text_analyzer import TextAnalyzer  
from image_analyzer import ImageAnalyzer


class TestAIApplicationsIntegration:
    """Integration tests for all AI applications working together."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.chatbot = AIchatbot()
        self.text_analyzer = TextAnalyzer()
        self.image_analyzer = ImageAnalyzer()
    
    def test_all_applications_initialize(self):
        """Test that all applications can be initialized together."""
        assert isinstance(self.chatbot, AIchatbot)
        assert isinstance(self.text_analyzer, TextAnalyzer)
        assert isinstance(self.image_analyzer, ImageAnalyzer)
        
        # Test they don't interfere with each other
        assert hasattr(self.chatbot, 'responses')
        assert hasattr(self.text_analyzer, 'positive_words')
        assert hasattr(self.image_analyzer, 'color_ranges')
    
    def test_chatbot_text_analysis_integration(self):
        """Test integration between chatbot and text analysis."""
        # Get chatbot response
        response = self.chatbot.get_response("This is amazing and wonderful!")
        
        # Analyze the chatbot's response
        analysis = self.text_analyzer.analyze_text(response)
        
        assert isinstance(response, str)
        assert len(response) > 0
        assert isinstance(analysis, dict)
        assert analysis['statistics']['word_count'] > 0
        
        # Chatbot responses should generally be neutral or positive
        sentiment = analysis['sentiment']['label']
        assert sentiment in ['neutral', 'positive', 'negative']  # Any is acceptable
    
    def test_cross_application_workflow(self):
        """Test a realistic workflow using multiple applications."""
        # Step 1: User asks chatbot about AI
        ai_question = "What are AI applications in image processing?"
        bot_response = self.chatbot.get_response(ai_question)
        
        # Step 2: Analyze the bot's response text
        text_analysis = self.text_analyzer.analyze_text(bot_response)
        
        # Step 3: Create and analyze a sample image
        sample_image = self.image_analyzer.create_sample_image(10, 10, 'gradient')
        image_analysis = self.image_analyzer.analyze_image_data(sample_image)
        
        # Verify all steps worked
        assert isinstance(bot_response, str)
        assert len(bot_response) > 20  # Substantial response
        
        assert text_analysis['statistics']['word_count'] > 5
        # Should contain AI-related keywords in top words
        word_freq = text_analysis['word_frequency']
        common_words = [w['word'] for w in word_freq['most_common_words'][:5]]
        
        ai_keywords = ['ai', 'applications', 'virtual', 'systems', 'image', 'recognition']
        keywords_found = any(keyword in common_words for keyword in ai_keywords)
        assert keywords_found
        
        assert image_analysis['dimensions']['total_pixels'] == 100
        assert len(image_analysis['summary']) > 10
    
    def test_data_flow_between_applications(self):
        """Test data flowing from one application to another."""
        # Generate conversation history
        conversation_topics = [
            "Hello, I'm interested in AI",
            "What is machine learning?",
            "How does computer vision work?",
            "Thank you for the information"
        ]
        
        responses = []
        for topic in conversation_topics:
            response = self.chatbot.get_response(topic)
            responses.append(response)
        
        # Combine all responses into a single text
        combined_text = " ".join(responses)
        
        # Analyze the combined conversation
        conversation_analysis = self.text_analyzer.analyze_text(combined_text)
        
        # Should contain AI-related keywords
        word_freq = conversation_analysis['word_frequency']
        common_words = [w['word'] for w in word_freq['most_common_words']]
        
        ai_keywords = ['ai', 'machine', 'learning', 'computer', 'vision', 'intelligence']
        keywords_found = any(keyword in ' '.join(common_words) for keyword in ai_keywords)
        
        assert keywords_found
        assert conversation_analysis['statistics']['word_count'] > 35
    
    def test_error_handling_across_applications(self):
        """Test error handling when applications receive invalid input."""
        # Test empty/invalid inputs across all applications
        invalid_inputs = [None, "", "   ", []]
        
        for invalid_input in invalid_inputs:
            # Chatbot should handle gracefully
            if invalid_input is None:
                bot_response = self.chatbot.get_response(invalid_input)
            else:
                bot_response = self.chatbot.get_response(str(invalid_input))
            assert isinstance(bot_response, str)
            assert len(bot_response) > 0
            
            # Text analyzer should handle gracefully
            text_analysis = self.text_analyzer.analyze_text(invalid_input)
            assert 'statistics' in text_analysis
            assert text_analysis['statistics']['word_count'] == 0
            
            # Image analyzer should handle gracefully
            image_analysis = self.image_analyzer.analyze_image_data(invalid_input)
            assert 'error' in image_analysis or image_analysis['dimensions']['total_pixels'] == 0
    
    def test_performance_with_realistic_data(self):
        """Test performance with realistic data sizes."""
        # Large text analysis
        large_text = """
        Artificial Intelligence (AI) has revolutionized numerous industries and continues to shape our world 
        in unprecedented ways. Machine learning algorithms can now process vast amounts of data, identify 
        patterns, and make predictions with remarkable accuracy. Computer vision systems can analyze images 
        and videos, enabling applications like autonomous vehicles, medical diagnosis, and security systems.
        
        Natural Language Processing (NLP) has made it possible for machines to understand and generate 
        human language, powering virtual assistants, translation services, and content creation tools. 
        Deep learning neural networks, inspired by the human brain, have achieved breakthroughs in areas 
        such as image recognition, speech synthesis, and game playing.
        
        However, AI also presents challenges including ethical considerations, job displacement concerns, 
        privacy issues, and the need for responsible development. As we advance in this field, it's crucial 
        to ensure that AI benefits humanity while mitigating potential risks.
        """ * 3  # Make it even larger
        
        # Test all applications can handle it
        text_analysis = self.text_analyzer.analyze_text(large_text)
        assert text_analysis['statistics']['word_count'] > 300
        
        # Large image
        large_image = self.image_analyzer.create_sample_image(25, 25, 'random')
        image_analysis = self.image_analyzer.analyze_image_data(large_image)
        assert image_analysis['dimensions']['total_pixels'] == 625
        
        # Multiple chatbot interactions
        for i in range(10):
            response = self.chatbot.get_response(f"Question number {i} about AI")
            assert isinstance(response, str)
        
        history = self.chatbot.get_conversation_history()
        assert len(history) == 10
    
    def test_memory_usage_and_cleanup(self):
        """Test that applications don't accumulate excessive memory."""
        initial_history_length = len(self.chatbot.get_conversation_history())
        
        # Perform many operations
        for i in range(100):
            # Short operations to avoid excessive test time
            self.chatbot.get_response("hi")
            
            small_text = f"Test text number {i} with good sentiment."
            self.text_analyzer.analyze_text(small_text)
            
            if i % 20 == 0:  # Only create images occasionally
                small_image = self.image_analyzer.create_sample_image(3, 3, 'random')
                self.image_analyzer.analyze_image_data(small_image)
        
        # Memory should be manageable (chatbot accumulates history)
        final_history_length = len(self.chatbot.get_conversation_history())
        assert final_history_length == initial_history_length + 100
        
        # Clear history to test cleanup
        self.chatbot.clear_history()
        assert len(self.chatbot.get_conversation_history()) == 0


class TestWebInterfaceIntegration:
    """Test the web interface functionality."""
    
    def test_html_file_exists(self):
        """Test that the HTML interface file exists and is readable."""
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution', 'index.html')
        
        assert os.path.exists(html_path)
        
        with open(html_path, 'r') as f:
            content = f.read()
        
        # Check for key elements
        assert 'AI Applications Workshop' in content
        assert 'chatbot' in content.lower()
        assert 'text analyzer' in content.lower()
        assert 'image analyzer' in content.lower()
        assert 'javascript' in content.lower() or 'script' in content.lower()
    
    def test_html_structure(self):
        """Test HTML structure and required elements."""
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution', 'index.html')
        
        with open(html_path, 'r') as f:
            content = f.read()
        
        # Check for required HTML elements
        required_elements = [
            '<html',
            '<head>',
            '<body>',
            '<script>',
            'function sendChatMessage',
            'function analyzeText',
            'function analyzeImage'
        ]
        
        for element in required_elements:
            assert element in content, f"Missing required element: {element}"
    
    def test_javascript_functions_defined(self):
        """Test that required JavaScript functions are defined."""
        html_path = os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution', 'index.html')
        
        with open(html_path, 'r') as f:
            content = f.read()
        
        # Check for key JavaScript functions
        js_functions = [
            'sendChatMessage',
            'generateChatResponse',
            'analyzeText',
            'performTextAnalysis',
            'analyzeImage',
            'generateSampleImage',
            'performImageAnalysis'
        ]
        
        for func in js_functions:
            assert f'function {func}' in content, f"Missing JavaScript function: {func}"


class TestEndToEndScenarios:
    """End-to-end test scenarios simulating real user interactions."""
    
    def test_ai_learning_session_scenario(self):
        """Simulate a complete AI learning session."""
        chatbot = AIchatbot()
        text_analyzer = TextAnalyzer()
        image_analyzer = ImageAnalyzer()
        
        # Scenario: Student learning about AI
        learning_session = [
            # Introduction
            ("Hello, I want to learn about AI", "greeting"),
            ("What is artificial intelligence?", "ai_definition"),
            ("Can you explain machine learning?", "machine_learning"),
            ("What are some AI applications?", "applications"),
        ]
        
        session_responses = []
        for question, expected_type in learning_session:
            response = chatbot.get_response(question)
            session_responses.append(response)
            
            # Verify response type
            history = chatbot.get_conversation_history()
            assert history[-1]['response_type'] == expected_type
        
        # Analyze the learning session content
        full_session = " ".join(session_responses)
        session_analysis = text_analyzer.analyze_text(full_session)
        
        # Should be informative (many words) and educational (positive/neutral)
        assert session_analysis['statistics']['word_count'] > 40
        assert session_analysis['sentiment']['label'] in ['positive', 'neutral']
        
        # Should contain educational keywords
        common_words = [w['word'] for w in session_analysis['word_frequency']['most_common_words']]
        educational_terms = ['ai', 'artificial', 'intelligence', 'machine', 'learning', 'data']
        assert any(term in ' '.join(common_words) for term in educational_terms)
        
        # Demonstrate image analysis capabilities
        demo_images = ['gradient', 'checkerboard', 'random']
        for pattern in demo_images:
            image = image_analyzer.create_sample_image(8, 8, pattern)
            analysis = image_analyzer.analyze_image_data(image)
            
            assert 'error' not in analysis
            assert analysis['dimensions']['total_pixels'] == 64
            
            if pattern == 'checkerboard':
                assert 'checkerboard' in analysis['patterns']['detected_patterns']
    
    def test_content_creation_scenario(self):
        """Simulate using AI tools for content creation and analysis."""
        text_analyzer = TextAnalyzer()
        
        # Scenario: Content creator analyzing different types of content
        content_samples = [
            ("Amazing product review! This is excellent, wonderful, and fantastic!", "positive"),
            ("Terrible experience. This was awful, horrible, and disappointing.", "negative"),
            ("The technical specifications include advanced algorithms and robust architecture.", "neutral"),
            ("Mixed feelings: good features but bad usability. Love the design, hate the interface.", "mixed")
        ]
        
        analysis_results = []
        for content, expected_sentiment_type in content_samples:
            analysis = text_analyzer.analyze_text(content)
            analysis_results.append(analysis)
            
            # Verify sentiment detection works reasonably
            sentiment = analysis['sentiment']['label']
            
            if expected_sentiment_type == "positive":
                assert sentiment == 'positive'
            elif expected_sentiment_type == "negative":
                assert sentiment == 'negative'
            elif expected_sentiment_type == "neutral":
                assert sentiment == 'neutral'
            # Mixed sentiment could go either way
        
        # Verify all analyses completed successfully
        for analysis in analysis_results:
            assert 'statistics' in analysis
            assert 'sentiment' in analysis
            assert 'word_frequency' in analysis
            assert analysis['statistics']['word_count'] > 0
    
    def test_educational_demo_scenario(self):
        """Simulate an educational demo of AI capabilities."""
        chatbot = AIchatbot()
        text_analyzer = TextAnalyzer()
        image_analyzer = ImageAnalyzer()
        
        # Demo script
        demo_steps = [
            # Step 1: Introduction
            "Hello, welcome to our AI demo",
            
            # Step 2: Ask about AI
            "What can you tell me about AI applications in education?",
            
            # Step 3: Demonstrate text analysis
            "Let's analyze this text: AI is transforming education through personalized learning, intelligent tutoring systems, and automated assessment tools.",
            
            # Step 4: Demonstrate image analysis
            # (Create sample images)
            
            # Step 5: Wrap up
            "Thank you for the demonstration"
        ]
        
        demo_results = {}
        
        # Chatbot interactions
        for i, step in enumerate(demo_steps[:2] + demo_steps[4:]):  # Skip step 3 for now
            response = chatbot.get_response(step)
            demo_results[f'chatbot_step_{i}'] = response
            assert isinstance(response, str)
            assert len(response) > 10
        
        # Text analysis demonstration
        demo_text = "AI is transforming education through personalized learning, intelligent tutoring systems, and automated assessment tools."
        text_analysis = text_analyzer.analyze_text(demo_text)
        demo_results['text_analysis'] = text_analysis
        
        assert text_analysis['statistics']['word_count'] > 10
        assert 'ai' in [w['word'] for w in text_analysis['word_frequency']['most_common_words'][:5]]
        
        # Image analysis demonstration
        demo_patterns = ['gradient', 'checkerboard', 'red_square']
        for pattern in demo_patterns:
            image = image_analyzer.create_sample_image(6, 6, pattern)
            analysis = image_analyzer.analyze_image_data(image)
            demo_results[f'image_analysis_{pattern}'] = analysis
            
            assert 'error' not in analysis
            assert analysis['dimensions']['total_pixels'] == 36
        
        # Verify complete demo results
        assert len(demo_results) >= 6  # At least 6 components demonstrated
    
    def test_stress_testing_scenario(self):
        """Test applications under stress conditions."""
        chatbot = AIchatbot()
        text_analyzer = TextAnalyzer()
        image_analyzer = ImageAnalyzer()
        
        # Stress test with rapid interactions
        for i in range(50):  # Reduced for faster testing
            # Rapid chatbot interactions
            response = chatbot.get_response(f"Question {i} about AI and machine learning")
            assert isinstance(response, str)
            
            # Rapid text analysis
            if i % 5 == 0:  # Every 5th iteration
                analysis = text_analyzer.analyze_text(f"Sample text {i} with various sentiments and words.")
                assert analysis['statistics']['word_count'] > 0
            
            # Occasional image analysis
            if i % 10 == 0:  # Every 10th iteration
                image = image_analyzer.create_sample_image(4, 4, 'random')
                img_analysis = image_analyzer.analyze_image_data(image)
                assert img_analysis['dimensions']['total_pixels'] == 16
        
        # Verify system state after stress test
        history = chatbot.get_conversation_history()
        assert len(history) == 50
        
        # Test cleanup capabilities
        chatbot.clear_history()
        assert len(chatbot.get_conversation_history()) == 0


class TestApplicationPersistence:
    """Test data persistence and state management across applications."""
    
    def test_conversation_persistence(self):
        """Test that conversation state persists correctly."""
        chatbot = AIchatbot()
        
        # Build up conversation history
        questions = [
            "Hello",
            "What is machine learning?",
            "How does AI work?", 
            "What are neural networks?",
            "Thank you"
        ]
        
        for question in questions:
            chatbot.get_response(question)
        
        history = chatbot.get_conversation_history()
        assert len(history) == 5
        
        # Verify conversation order is preserved
        for i, question in enumerate(questions):
            assert history[i]['user_input'] == question.lower()
        
        # Test that conversation context is maintained
        assert any('greeting' in entry['response_type'] for entry in history)
        assert any('machine_learning' in entry['response_type'] for entry in history)
    
    def test_analyzer_consistency(self):
        """Test that analyzers produce consistent results."""
        text_analyzer = TextAnalyzer()
        image_analyzer = ImageAnalyzer()
        
        # Test text analysis consistency
        test_text = "This is a wonderful and amazing example of great text analysis!"
        
        results = []
        for _ in range(5):
            analysis = text_analyzer.analyze_text(test_text)
            results.append(analysis)
        
        # All results should be identical
        base_result = results[0]
        for result in results[1:]:
            assert result['statistics'] == base_result['statistics']
            assert result['sentiment'] == base_result['sentiment']
            assert result['word_frequency'] == base_result['word_frequency']
        
        # Test image analysis consistency
        test_image = image_analyzer.create_sample_image(5, 5, 'gradient')
        
        image_results = []
        for _ in range(3):
            analysis = image_analyzer.analyze_image_data(test_image)
            image_results.append(analysis)
        
        # Results should be identical for same input
        base_image_result = image_results[0]
        for result in image_results[1:]:
            assert result['dimensions'] == base_image_result['dimensions']
            assert result['colors'] == base_image_result['colors']
            assert result['brightness'] == base_image_result['brightness']


if __name__ == '__main__':
    pytest.main([__file__])