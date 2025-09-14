"""
Simple Text Analysis AI Application  
Performs sentiment analysis and text statistics on user input.
"""

import re
from typing import Dict, List, Tuple, Optional
from collections import Counter
import math


class TextAnalyzer:
    """A simple text analysis tool with basic NLP capabilities."""
    
    def __init__(self):
        """Initialize the text analyzer with sentiment dictionaries."""
        # Simple sentiment word lists for educational purposes
        self.positive_words = {
            'amazing', 'awesome', 'fantastic', 'great', 'excellent', 'wonderful',
            'good', 'beautiful', 'love', 'like', 'happy', 'joy', 'brilliant',
            'perfect', 'outstanding', 'superb', 'marvelous', 'incredible',
            'fantastic', 'delighted', 'pleased', 'satisfied', 'excited'
        }
        
        self.negative_words = {
            'terrible', 'awful', 'horrible', 'bad', 'worst', 'hate', 'dislike',
            'sad', 'angry', 'frustrated', 'disappointed', 'annoyed', 'upset',
            'disgusting', 'pathetic', 'useless', 'boring', 'stupid', 'ridiculous',
            'annoying', 'irritating', 'unpleasant', 'dreadful'
        }
        
        # Common stop words for text analysis
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
            'could', 'can', 'may', 'might', 'must', 'i', 'you', 'he', 'she', 'it',
            'we', 'they', 'me', 'him', 'her', 'us', 'them', 'my', 'your', 'his',
            'her', 'its', 'our', 'their', 'this', 'that', 'these', 'those'
        }
    
    def analyze_text(self, text: str) -> Dict:
        """
        Perform comprehensive text analysis.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            Dict: Analysis results containing statistics and sentiment
        """
        if not text or not text.strip():
            return self._empty_analysis()
        
        # Clean and preprocess text
        cleaned_text = self._clean_text(text)
        words = self._tokenize(cleaned_text)
        
        # Basic statistics
        stats = self._calculate_statistics(text, words)
        
        # Sentiment analysis
        sentiment = self._analyze_sentiment(words)
        
        # Word frequency analysis
        word_freq = self._calculate_word_frequency(words)
        
        # Readability metrics
        readability = self._calculate_readability(text, words)
        
        return {
            'statistics': stats,
            'sentiment': sentiment,
            'word_frequency': word_freq,
            'readability': readability,
            'summary': self._generate_summary(stats, sentiment)
        }
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Convert to lowercase and remove extra whitespace
        text = text.lower().strip()
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\!\?\,\;\:]', ' ', text)
        # Replace multiple spaces with single space
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def _tokenize(self, text: str) -> List[str]:
        """Tokenize text into words."""
        # Split by whitespace and punctuation
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if len(word) > 1]
    
    def _calculate_statistics(self, original_text: str, words: List[str]) -> Dict:
        """Calculate basic text statistics."""
        sentences = re.split(r'[.!?]+', original_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        paragraphs = original_text.split('\n\n')
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        
        return {
            'character_count': len(original_text),
            'character_count_no_spaces': len(original_text.replace(' ', '')),
            'word_count': len(words),
            'sentence_count': len(sentences),
            'paragraph_count': len(paragraphs),
            'average_word_length': round(sum(len(word) for word in words) / len(words), 2) if words else 0,
            'average_words_per_sentence': round(len(words) / len(sentences), 2) if sentences else 0
        }
    
    def _analyze_sentiment(self, words: List[str]) -> Dict:
        """Analyze sentiment of text."""
        positive_count = sum(1 for word in words if word in self.positive_words)
        negative_count = sum(1 for word in words if word in self.negative_words)
        total_sentiment_words = positive_count + negative_count
        
        if total_sentiment_words == 0:
            sentiment_score = 0.0
            sentiment_label = 'neutral'
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
            if sentiment_score > 0.3:
                sentiment_label = 'positive'
            elif sentiment_score < -0.3:
                sentiment_label = 'negative'
            else:
                sentiment_label = 'neutral'
        
        return {
            'score': round(sentiment_score, 3),
            'label': sentiment_label,
            'positive_words_found': positive_count,
            'negative_words_found': negative_count,
            'confidence': min(total_sentiment_words / len(words) * 2, 1.0) if words else 0.0
        }
    
    def _calculate_word_frequency(self, words: List[str]) -> Dict:
        """Calculate word frequency excluding stop words."""
        # Filter out stop words
        content_words = [word for word in words if word not in self.stop_words]
        
        # Count frequencies
        word_counts = Counter(content_words)
        total_words = len(content_words)
        
        # Get top 10 most common words
        most_common = word_counts.most_common(10)
        
        return {
            'total_unique_words': len(word_counts),
            'most_common_words': [
                {'word': word, 'count': count, 'frequency': round(count/total_words, 3)}
                for word, count in most_common
            ]
        }
    
    def _calculate_readability(self, text: str, words: List[str]) -> Dict:
        """Calculate basic readability metrics."""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences or not words:
            return {'flesch_reading_ease': 0, 'grade_level': 0}
        
        # Simplified syllable counting (rough approximation)
        syllables = sum(self._count_syllables(word) for word in words)
        
        # Flesch Reading Ease (simplified)
        avg_sentence_length = len(words) / len(sentences)
        avg_syllables_per_word = syllables / len(words)
        
        flesch_score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
        flesch_score = max(0, min(100, flesch_score))  # Clamp between 0-100
        
        # Estimate grade level
        grade_level = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
        grade_level = max(1, min(20, grade_level))  # Clamp between 1-20
        
        return {
            'flesch_reading_ease': round(flesch_score, 1),
            'estimated_grade_level': round(grade_level, 1),
            'avg_words_per_sentence': round(avg_sentence_length, 1),
            'avg_syllables_per_word': round(avg_syllables_per_word, 2)
        }
    
    def _count_syllables(self, word: str) -> int:
        """Count syllables in a word (simplified method)."""
        word = word.lower()
        if not word:
            return 0
        
        # Simple syllable counting heuristic
        vowels = 'aeiouy'
        syllable_count = 0
        prev_was_vowel = False
        
        for char in word:
            is_vowel = char in vowels
            if is_vowel and not prev_was_vowel:
                syllable_count += 1
            prev_was_vowel = is_vowel
        
        # Handle silent e
        if word.endswith('e') and syllable_count > 1:
            syllable_count -= 1
        
        # Ensure at least 1 syllable
        return max(1, syllable_count)
    
    def _generate_summary(self, stats: Dict, sentiment: Dict) -> str:
        """Generate a human-readable summary of the analysis."""
        word_count = stats['word_count']
        sentiment_label = sentiment['label']
        
        if word_count == 0:
            return "No text to analyze."
        
        summary_parts = []
        
        # Length assessment
        if word_count < 10:
            summary_parts.append("This is a very short text")
        elif word_count < 50:
            summary_parts.append("This is a short text")
        elif word_count < 200:
            summary_parts.append("This is a medium-length text")
        else:
            summary_parts.append("This is a long text")
        
        summary_parts.append(f"with {word_count} words")
        
        # Sentiment assessment
        if sentiment_label != 'neutral':
            confidence = sentiment['confidence']
            if confidence > 0.1:
                summary_parts.append(f"and has a {sentiment_label} tone")
        
        return " ".join(summary_parts) + "."
    
    def _empty_analysis(self, reason: str = "No text to analyze.") -> Dict:
        """Return empty analysis for invalid input."""
        return {
            'statistics': {
                'character_count': 0,
                'character_count_no_spaces': 0,
                'word_count': 0,
                'sentence_count': 0,
                'paragraph_count': 0,
                'average_word_length': 0,
                'average_words_per_sentence': 0
            },
            'sentiment': {
                'score': 0.0,
                'label': 'neutral',
                'positive_words_found': 0,
                'negative_words_found': 0,
                'confidence': 0.0
            },
            'word_frequency': {
                'total_unique_words': 0,
                'most_common_words': []
            },
            'readability': {
                'flesch_reading_ease': 0,
                'estimated_grade_level': 0,
                'avg_words_per_sentence': 0,
                'avg_syllables_per_word': 0
            },
            'summary': reason
        }


def main():
    """Main function to run the text analyzer interactively."""
    analyzer = TextAnalyzer()
    
    print("📝 Text Analyzer AI initialized!")
    print("Enter text to analyze, or 'quit' to exit.\n")
    
    while True:
        try:
            print("Enter text to analyze:")
            text = input("> ").strip()
            
            if text.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if not text:
                print("Please enter some text to analyze.\n")
                continue
            
            analysis = analyzer.analyze_text(text)
            
            print("\n" + "="*50)
            print("ANALYSIS RESULTS")
            print("="*50)
            
            # Statistics
            stats = analysis['statistics']
            print(f"📊 Statistics:")
            print(f"   Words: {stats['word_count']}")
            print(f"   Characters: {stats['character_count']}")
            print(f"   Sentences: {stats['sentence_count']}")
            print(f"   Average word length: {stats['average_word_length']}")
            
            # Sentiment
            sentiment = analysis['sentiment']
            print(f"\n😊 Sentiment: {sentiment['label'].upper()}")
            print(f"   Score: {sentiment['score']}")
            print(f"   Confidence: {sentiment['confidence']:.1%}")
            
            # Top words
            word_freq = analysis['word_frequency']
            if word_freq['most_common_words']:
                print(f"\n🔤 Top words:")
                for word_info in word_freq['most_common_words'][:5]:
                    print(f"   {word_info['word']}: {word_info['count']} times")
            
            # Readability
            readability = analysis['readability']
            print(f"\n📖 Readability:")
            print(f"   Grade level: {readability['estimated_grade_level']}")
            print(f"   Reading ease: {readability['flesch_reading_ease']}")
            
            # Summary
            print(f"\n💬 Summary: {analysis['summary']}")
            
            print("\n" + "="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}\n")


if __name__ == "__main__":
    main()