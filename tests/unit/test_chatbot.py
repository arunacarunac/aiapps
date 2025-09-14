"""
Unit tests for the AI Chatbot Application.
Tests all core functionality including response generation, pattern matching,
conversation history, and custom response features.
"""

import pytest
import sys
import os

# Add the solution directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution'))

from chatbot_app import AIchatbot


class TestAIchatbot:
    """Test class for AI Chatbot functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.chatbot = AIchatbot()
    
    def test_initialization(self):
        """Test that chatbot initializes properly."""
        assert isinstance(self.chatbot, AIchatbot)
        assert hasattr(self.chatbot, 'responses')
        assert hasattr(self.chatbot, 'patterns')
        assert hasattr(self.chatbot, 'conversation_history')
        assert len(self.chatbot.conversation_history) == 0
    
    def test_greeting_responses(self):
        """Test that greeting inputs generate appropriate responses."""
        greeting_inputs = ['hello', 'hi', 'hey', 'Hello there!', 'Hi how are you']
        
        for greeting in greeting_inputs:
            response = self.chatbot.get_response(greeting)
            assert isinstance(response, str)
            assert len(response) > 0
            # Check if response contains expected greeting keywords or is welcoming
            assert any(word in response.lower() for word in ['hello', 'hi', 'help', 'assist', 'welcome', 'feel', 'free'])
    
    def test_ai_definition_responses(self):
        """Test responses to AI definition questions."""
        ai_questions = [
            'what is ai',
            'define ai',
            'ai definition',
            'What is artificial intelligence?'
        ]
        
        for question in ai_questions:
            response = self.chatbot.get_response(question)
            assert isinstance(response, str)
            assert len(response) > 0
            # Check if response contains AI-related terms
            assert any(term in response.lower() for term in ['ai', 'artificial', 'intelligence', 'machine'])
    
    def test_machine_learning_responses(self):
        """Test responses to machine learning questions."""
        ml_questions = [
            'machine learning',
            'what is ml',
            'learn from data',
            'Machine Learning algorithms'
        ]
        
        for question in ml_questions:
            response = self.chatbot.get_response(question)
            assert isinstance(response, str)
            assert len(response) > 0
            # Check if response contains ML-related terms
            assert any(term in response.lower() for term in ['machine learning', 'ml', 'data', 'learn'])
    
    def test_applications_responses(self):
        """Test responses to AI applications questions."""
        app_questions = [
            'ai applications',
            'where is ai used',
            'ai examples',
            'What are some AI applications?'
        ]
        
        for question in app_questions:
            response = self.chatbot.get_response(question)
            assert isinstance(response, str)
            assert len(response) > 0
            # Check if response contains application examples
            assert any(term in response.lower() for term in ['applications', 'used', 'virtual', 'recommendation', 'powers', 'search', 'social', 'autonomous'])
    
    def test_goodbye_responses(self):
        """Test goodbye responses."""
        goodbye_inputs = ['goodbye', 'bye', 'see you', 'thanks for your help']
        
        for goodbye in goodbye_inputs:
            response = self.chatbot.get_response(goodbye)
            assert isinstance(response, str)
            assert len(response) > 0
            # Check if response contains farewell terms
            assert any(word in response.lower() for word in ['goodbye', 'bye', 'thanks', 'farewell', 'see', 'later', 'hope', 'helpful'])
    
    def test_default_responses(self):
        """Test default responses for unrecognized input."""
        unknown_inputs = [
            'random nonsense text',
            'xyz123',
            'completely unrelated question',
            'blah blah blah'
        ]
        
        for unknown in unknown_inputs:
            response = self.chatbot.get_response(unknown)
            assert isinstance(response, str)
            assert len(response) > 0
            # Default responses should ask for clarification
            assert any(word in response.lower() for word in ['question', 'specific', 'understand', 'rephrase', 'interesting', 'could', 'sure', 'help', 'context'])
    
    def test_empty_input_handling(self):
        """Test handling of empty or whitespace-only input."""
        empty_inputs = ['', '   ', '\t', '\n', None]
        
        for empty_input in empty_inputs[:4]:  # Skip None for now
            response = self.chatbot.get_response(empty_input)
            assert isinstance(response, str)
            assert 'input' in response.lower()
    
    def test_none_input_handling(self):
        """Test handling of None input."""
        response = self.chatbot.get_response(None)
        assert isinstance(response, str)
        assert 'input' in response.lower()
    
    def test_conversation_history_tracking(self):
        """Test that conversation history is properly tracked."""
        initial_length = len(self.chatbot.conversation_history)
        
        # Send a message
        response = self.chatbot.get_response("hello")
        
        # Check that history increased
        assert len(self.chatbot.conversation_history) == initial_length + 1
        
        # Check history entry format
        history_entry = self.chatbot.conversation_history[-1]
        assert 'timestamp' in history_entry
        assert 'user_input' in history_entry
        assert 'response_type' in history_entry
        assert 'bot_response' in history_entry
        
        assert history_entry['user_input'] == 'hello'
        assert history_entry['bot_response'] == response
        assert history_entry['response_type'] == 'greeting'
    
    def test_get_conversation_history(self):
        """Test getting conversation history."""
        # Initially empty
        history = self.chatbot.get_conversation_history()
        assert isinstance(history, list)
        assert len(history) == 0
        
        # Add some conversations
        self.chatbot.get_response("hello")
        self.chatbot.get_response("what is ai")
        
        history = self.chatbot.get_conversation_history()
        assert len(history) == 2
        
        # Ensure it's a copy (not the original)
        history.append({'test': 'entry'})
        assert len(self.chatbot.get_conversation_history()) == 2
    
    def test_clear_history(self):
        """Test clearing conversation history."""
        # Add some conversations
        self.chatbot.get_response("hello")
        self.chatbot.get_response("goodbye")
        
        assert len(self.chatbot.conversation_history) > 0
        
        # Clear history
        self.chatbot.clear_history()
        
        assert len(self.chatbot.conversation_history) == 0
        assert len(self.chatbot.get_conversation_history()) == 0
    
    def test_add_custom_response_valid(self):
        """Test adding valid custom responses."""
        pattern = r'\btest\s+pattern\b'
        response_type = 'test_response'
        responses = ['Test response 1', 'Test response 2']
        
        result = self.chatbot.add_custom_response(pattern, response_type, responses)
        
        assert result is True
        assert response_type in self.chatbot.patterns
        assert pattern in self.chatbot.patterns[response_type]
        assert response_type in self.chatbot.responses
        assert all(resp in self.chatbot.responses[response_type] for resp in responses)
        
        # Test that custom response works
        response = self.chatbot.get_response("test pattern")
        assert response in responses
    
    def test_add_custom_response_invalid_pattern(self):
        """Test adding custom response with invalid regex pattern."""
        invalid_pattern = r'[invalid regex pattern'  # Missing closing bracket
        response_type = 'invalid_test'
        responses = ['Invalid response']
        
        result = self.chatbot.add_custom_response(invalid_pattern, response_type, responses)
        
        assert result is False
        assert response_type not in self.chatbot.patterns
    
    def test_case_insensitive_matching(self):
        """Test that input matching is case insensitive."""
        test_cases = [
            ('HELLO', 'greeting'),
            ('What Is AI', 'ai_definition'),
            ('MACHINE LEARNING', 'machine_learning'),
            ('AI APPLICATIONS', 'applications'),
            ('GOODBYE', 'goodbye')
        ]
        
        for input_text, expected_type in test_cases:
            # Clear history to isolate test
            self.chatbot.clear_history()
            
            response = self.chatbot.get_response(input_text)
            
            # Check that response was generated and classified correctly
            assert isinstance(response, str)
            assert len(response) > 0
            
            history = self.chatbot.get_conversation_history()
            assert len(history) == 1
            assert history[0]['response_type'] == expected_type
    
    def test_input_classification(self):
        """Test the internal input classification method."""
        test_cases = [
            ('hello there', 'greeting'),
            ('what is artificial intelligence', 'ai_definition'),
            ('machine learning algorithms', 'machine_learning'),
            ('ai applications in healthcare', 'applications'),
            ('goodbye friend', 'goodbye'),
            ('random unrelated text', 'default')
        ]
        
        for input_text, expected_type in test_cases:
            classified_type = self.chatbot._classify_input(input_text)
            assert classified_type == expected_type
    
    def test_response_randomness(self):
        """Test that responses vary when multiple options are available."""
        # Get multiple responses for the same input
        responses = []
        for _ in range(20):  # Get 20 responses
            response = self.chatbot.get_response("hello")
            responses.append(response)
        
        # Should get some variation in responses (not all identical)
        unique_responses = set(responses)
        assert len(unique_responses) > 1 or len(self.chatbot.responses['greeting']) == 1
    
    def test_whitespace_handling(self):
        """Test proper handling of whitespace in input."""
        test_inputs = [
            '  hello  ',
            '\thello\t',
            '\nhello\n',
            '  what   is   ai  '
        ]
        
        for input_with_whitespace in test_inputs:
            response = self.chatbot.get_response(input_with_whitespace)
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Check that input was properly cleaned in history
            history = self.chatbot.get_conversation_history()
            last_entry = history[-1]
            assert last_entry['user_input'] == input_with_whitespace.lower().strip()
    
    def test_conversation_flow(self):
        """Test a complete conversation flow."""
        conversation_flow = [
            ('hello', 'greeting'),
            ('what is ai', 'ai_definition'),
            ('tell me about machine learning', 'machine_learning'),
            ('what are some ai applications', 'applications'),
            ('goodbye', 'goodbye')
        ]
        
        for i, (input_text, expected_type) in enumerate(conversation_flow):
            response = self.chatbot.get_response(input_text)
            
            assert isinstance(response, str)
            assert len(response) > 0
            
            # Check history length
            history = self.chatbot.get_conversation_history()
            assert len(history) == i + 1
            
            # Check last entry
            last_entry = history[-1]
            assert last_entry['response_type'] == expected_type
            assert last_entry['user_input'] == input_text.lower()
            assert last_entry['bot_response'] == response
    
    def test_pattern_matching_priority(self):
        """Test that pattern matching works correctly with overlapping patterns."""
        # Test input that could match multiple patterns
        test_input = "hello, what is ai and machine learning"
        
        response = self.chatbot.get_response(test_input)
        history = self.chatbot.get_conversation_history()
        
        # Should match the first pattern found (greeting in this case)
        assert history[-1]['response_type'] == 'greeting'
    
    def test_error_handling_in_response_selection(self):
        """Test error handling in response selection."""
        # Temporarily corrupt responses to test error handling
        original_responses = self.chatbot.responses.copy()
        
        try:
            # Test with empty responses list
            self.chatbot.responses['greeting'] = []
            response = self.chatbot.get_response("hello")
            assert isinstance(response, str)
            
        finally:
            # Restore original responses
            self.chatbot.responses = original_responses


class TestChatbotIntegration:
    """Integration tests for chatbot functionality."""
    
    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        from chatbot_app import main
        assert callable(main)
    
    def test_multiple_chatbot_instances(self):
        """Test that multiple chatbot instances work independently."""
        chatbot1 = AIchatbot()
        chatbot2 = AIchatbot()
        
        # Add different custom responses
        chatbot1.add_custom_response(r'\btest1\b', 'test1', ['Response 1'])
        chatbot2.add_custom_response(r'\btest2\b', 'test2', ['Response 2'])
        
        # Test independence
        response1 = chatbot1.get_response("test1")
        response2 = chatbot2.get_response("test2")
        
        assert response1 == 'Response 1'
        assert response2 == 'Response 2'
        
        # Test that they don't share custom responses
        default_response1 = chatbot1.get_response("test2")
        default_response2 = chatbot2.get_response("test1")
        
        assert default_response1 != 'Response 2'
        assert default_response2 != 'Response 1'
    
    def test_conversation_persistence(self):
        """Test that conversation history persists across multiple interactions."""
        chatbot = AIchatbot()
        
        # Have a long conversation
        conversation = [
            "hello",
            "what is ai",
            "tell me about machine learning",
            "what are ai applications",
            "goodbye"
        ]
        
        for msg in conversation:
            chatbot.get_response(msg)
        
        history = chatbot.get_conversation_history()
        assert len(history) == len(conversation)
        
        # Check that all messages are preserved in order
        for i, original_msg in enumerate(conversation):
            assert history[i]['user_input'] == original_msg.lower()


if __name__ == '__main__':
    pytest.main([__file__])