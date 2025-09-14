"""
Simple AI Chatbot Application
A basic chatbot that can respond to user queries using simple pattern matching
and provide helpful responses about AI topics.
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime


class AIchatbot:
    """A simple AI chatbot for educational purposes."""
    
    def __init__(self):
        """Initialize the chatbot with predefined responses."""
        self.responses = {
            'greeting': [
                "Hello! I'm an AI chatbot. How can I help you today?",
                "Hi there! I'm here to assist you with AI-related questions.",
                "Welcome! Feel free to ask me about artificial intelligence."
            ],
            'ai_definition': [
                "AI (Artificial Intelligence) is the simulation of human intelligence in machines.",
                "Artificial Intelligence refers to systems that can perform tasks that typically require human intelligence.",
                "AI is technology that enables machines to learn, reason, and make decisions."
            ],
            'machine_learning': [
                "Machine Learning is a subset of AI that enables systems to learn from data.",
                "ML allows computers to improve their performance on tasks through experience.",
                "Machine Learning algorithms can identify patterns and make predictions from data."
            ],
            'applications': [
                "AI is used in healthcare, finance, transportation, entertainment, and many other fields.",
                "Common AI applications include virtual assistants, recommendation systems, and image recognition.",
                "AI powers search engines, social media feeds, and autonomous vehicles."
            ],
            'goodbye': [
                "Goodbye! Thanks for chatting with me about AI!",
                "See you later! Keep exploring the world of AI!",
                "Farewell! I hope I was helpful in answering your AI questions."
            ],
            'default': [
                "That's an interesting question! Could you be more specific?",
                "I'm not sure I understand. Could you rephrase your question?",
                "I'd love to help, but I need more context. What exactly would you like to know about AI?"
            ]
        }
        
        self.patterns = {
            'greeting': [r'\b(hello|hi|hey|greetings)\b', r'\bhow\s+are\s+you\b'],
            'ai_definition': [r'\bwhat\s+is\s+ai\b', r'\bdefine\s+ai\b', r'\bai\s+definition\b', r'\bwhat\s+is\s+artificial\s+intelligence\b', r'\bartificial\s+intelligence\b'],
            'machine_learning': [r'\bmachine\s+learning\b', r'\bml\b', r'\blearn.*data\b'],
            'applications': [r'\bai\s+applications\b', r'\bwhere.*ai.*used\b', r'\bai.*examples\b', r'\bapplications\s+of\s+ai\b'],
            'goodbye': [r'\b(goodbye|bye|see\s+you|farewell)\b', r'\bthanks?\s+(you\s+)?for\s+your\s+help\b']
        }
        
        self.conversation_history: List[Dict[str, str]] = []
    
    def get_response(self, user_input: str) -> str:
        """
        Generate a response based on user input.
        
        Args:
            user_input (str): The user's message
            
        Returns:
            str: The chatbot's response
        """
        if not user_input or not user_input.strip():
            return "I didn't receive any input. Please ask me something!"
        
        user_input = user_input.lower().strip()
        
        # Log the conversation
        timestamp = datetime.now().isoformat()
        
        # Find matching pattern
        response_type = self._classify_input(user_input)
        response = self._select_response(response_type)
        
        # Store conversation
        self.conversation_history.append({
            'timestamp': timestamp,
            'user_input': user_input,
            'response_type': response_type,
            'bot_response': response
        })
        
        return response
    
    def _classify_input(self, user_input: str) -> str:
        """
        Classify user input based on predefined patterns.
        
        Args:
            user_input (str): The processed user input
            
        Returns:
            str: The classified response type
        """
        for response_type, patterns in self.patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    return response_type
        
        return 'default'
    
    def _select_response(self, response_type: str) -> str:
        """
        Select a response from the available responses for the given type.
        
        Args:
            response_type (str): The type of response needed
            
        Returns:
            str: Selected response
        """
        import random
        responses = self.responses.get(response_type, self.responses['default'])
        
        # Handle empty responses list
        if not responses:
            return "I'm not sure how to respond to that. Could you try asking something else?"
        
        return random.choice(responses)
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List[Dict[str, str]]: List of conversation entries
        """
        return self.conversation_history.copy()
    
    def clear_history(self) -> None:
        """Clear the conversation history."""
        self.conversation_history.clear()
    
    def add_custom_response(self, pattern: str, response_type: str, responses: List[str]) -> bool:
        """
        Add a custom response pattern and responses.
        
        Args:
            pattern (str): Regex pattern to match
            response_type (str): Type identifier for the response
            responses (List[str]): List of possible responses
            
        Returns:
            bool: True if successfully added
        """
        try:
            # Validate pattern
            re.compile(pattern)
            
            # Add to patterns and responses
            if response_type not in self.patterns:
                self.patterns[response_type] = []
            if response_type not in self.responses:
                self.responses[response_type] = []
                
            self.patterns[response_type].append(pattern)
            self.responses[response_type].extend(responses)
            
            return True
        except re.error:
            return False


def main():
    """Main function to run the chatbot interactively."""
    chatbot = AIchatbot()
    
    print("🤖 AI Chatbot initialized! Type 'quit' to exit.")
    print("Ask me anything about artificial intelligence!\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Bot: Goodbye! Thanks for chatting!")
                break
            
            response = chatbot.get_response(user_input)
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\nBot: Goodbye! Thanks for chatting!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()