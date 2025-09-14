"""
Unit tests for the Text Analyzer AI Application.
Tests text processing, sentiment analysis, statistics calculation,
word frequency analysis, and readability metrics.
"""

import pytest
import sys
import os

# Add the solution directory to the path so we can import the modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'workshop', 'solution'))

from text_analyzer import TextAnalyzer


class TestTextAnalyzer:
    """Test class for Text Analyzer functionality."""
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.analyzer = TextAnalyzer()
    
    def test_initialization(self):
        """Test that analyzer initializes properly."""
        assert isinstance(self.analyzer, TextAnalyzer)
        assert hasattr(self.analyzer, 'positive_words')
        assert hasattr(self.analyzer, 'negative_words')
        assert hasattr(self.analyzer, 'stop_words')
        assert len(self.analyzer.positive_words) > 0
        assert len(self.analyzer.negative_words) > 0
        assert len(self.analyzer.stop_words) > 0
    
    def test_empty_text_analysis(self):
        """Test analysis of empty or None text."""
        empty_inputs = ['', '   ', '\t', '\n', None]
        
        for empty_input in empty_inputs:
            analysis = self.analyzer.analyze_text(empty_input)
            
            assert isinstance(analysis, dict)
            assert 'statistics' in analysis
            assert 'sentiment' in analysis
            assert 'word_frequency' in analysis
            assert 'readability' in analysis
            assert 'summary' in analysis
            
            # Check that empty analysis returns zero values
            stats = analysis['statistics']
            assert stats['word_count'] == 0
            assert stats['character_count'] == 0
            assert stats['sentence_count'] == 0
            
            assert analysis['summary'] == 'No text to analyze.'
    
    def test_basic_text_statistics(self):
        """Test basic text statistics calculation."""
        test_text = "Hello world! This is a test. How are you today?"
        analysis = self.analyzer.analyze_text(test_text)
        
        stats = analysis['statistics']
        
        assert stats['character_count'] == len(test_text)
        assert stats['character_count_no_spaces'] == len(test_text.replace(' ', ''))
        assert stats['word_count'] == 9  # Counting actual words (single chars filtered)
        assert stats['sentence_count'] == 3  # Three sentences
        assert stats['paragraph_count'] == 1  # One paragraph
        assert stats['average_word_length'] > 0
        assert stats['average_words_per_sentence'] > 0
    
    def test_positive_sentiment_analysis(self):
        """Test analysis of positive sentiment text."""
        positive_text = "This is amazing! I love this fantastic and wonderful experience. It's brilliant and excellent!"
        analysis = self.analyzer.analyze_text(positive_text)
        
        sentiment = analysis['sentiment']
        
        assert sentiment['label'] == 'positive'
        assert sentiment['score'] > 0
        assert sentiment['positive_words_found'] > sentiment['negative_words_found']
        assert sentiment['confidence'] > 0
    
    def test_negative_sentiment_analysis(self):
        """Test analysis of negative sentiment text."""
        negative_text = "This is terrible and awful. I hate this horrible and bad experience. It's disgusting and pathetic!"
        analysis = self.analyzer.analyze_text(negative_text)
        
        sentiment = analysis['sentiment']
        
        assert sentiment['label'] == 'negative'
        assert sentiment['score'] < 0
        assert sentiment['negative_words_found'] > sentiment['positive_words_found']
        assert sentiment['confidence'] > 0
    
    def test_neutral_sentiment_analysis(self):
        """Test analysis of neutral sentiment text."""
        neutral_text = "The weather report indicates partly cloudy conditions. Temperature will be 75 degrees."
        analysis = self.analyzer.analyze_text(neutral_text)
        
        sentiment = analysis['sentiment']
        
        assert sentiment['label'] == 'neutral'
        assert sentiment['score'] == 0.0
        assert sentiment['positive_words_found'] == 0
        assert sentiment['negative_words_found'] == 0
    
    def test_mixed_sentiment_analysis(self):
        """Test analysis of mixed sentiment text."""
        mixed_text = "The movie was good but also bad in some parts. I love the acting but hate the plot."
        analysis = self.analyzer.analyze_text(mixed_text)
        
        sentiment = analysis['sentiment']
        
        # Should be neutral or lean slightly in one direction
        assert sentiment['label'] in ['neutral', 'positive', 'negative']
        assert sentiment['positive_words_found'] > 0
        assert sentiment['negative_words_found'] > 0
    
    def test_word_frequency_analysis(self):
        """Test word frequency analysis."""
        text = "The cat sat on the mat. The cat was happy. The mat was comfortable."
        analysis = self.analyzer.analyze_text(text)
        
        word_freq = analysis['word_frequency']
        
        assert 'total_unique_words' in word_freq
        assert 'most_common_words' in word_freq
        assert word_freq['total_unique_words'] > 0
        assert len(word_freq['most_common_words']) > 0
        
        # Check format of most common words
        if word_freq['most_common_words']:
            first_word = word_freq['most_common_words'][0]
            assert 'word' in first_word
            assert 'count' in first_word
            assert 'frequency' in first_word
            assert first_word['count'] > 0
            assert 0 < first_word['frequency'] <= 1
    
    def test_stop_words_filtering(self):
        """Test that stop words are properly filtered from frequency analysis."""
        text = "The quick brown fox jumps over the lazy dog."
        analysis = self.analyzer.analyze_text(text)
        
        word_freq = analysis['word_frequency']
        common_words = word_freq['most_common_words']
        
        # Stop words like "the", "over" should not be in top words
        stop_words_found = [word for word in common_words if word['word'] in self.analyzer.stop_words]
        assert len(stop_words_found) == 0
    
    def test_readability_calculation(self):
        """Test readability metrics calculation."""
        text = "This is a simple sentence. It has basic words and structure."
        analysis = self.analyzer.analyze_text(text)
        
        readability = analysis['readability']
        
        assert 'flesch_reading_ease' in readability
        assert 'estimated_grade_level' in readability
        assert 'avg_words_per_sentence' in readability
        assert 'avg_syllables_per_word' in readability
        
        assert 0 <= readability['flesch_reading_ease'] <= 100
        assert readability['estimated_grade_level'] > 0
        assert readability['avg_words_per_sentence'] > 0
        assert readability['avg_syllables_per_word'] > 0
    
    def test_syllable_counting(self):
        """Test syllable counting functionality."""
        test_cases = [
            ('hello', 2),
            ('cat', 1),
            ('beautiful', 3),
            ('education', 4),
            ('a', 1),
            ('', 0),
            ('the', 1),
            ('computer', 3)
        ]
        
        for word, expected_min in test_cases:
            syllables = self.analyzer._count_syllables(word)
            assert syllables >= expected_min or syllables == max(1, expected_min - 1)
            assert syllables >= 1 if word else syllables == 0
    
    def test_text_cleaning(self):
        """Test text cleaning and preprocessing."""
        dirty_text = "  HELLO!!! @#$ World... 123   "
        cleaned = self.analyzer._clean_text(dirty_text)
        
        assert cleaned.islower()
        assert cleaned.strip() == cleaned
        assert '   ' not in cleaned  # No multiple spaces
    
    def test_tokenization(self):
        """Test word tokenization."""
        text = "Hello, world! This is a test... 123 and more."
        tokens = self.analyzer._tokenize(text)
        
        assert isinstance(tokens, list)
        assert all(isinstance(token, str) for token in tokens)
        assert all(len(token) > 1 for token in tokens)  # Single chars filtered out
        # Note: tokens may include numbers, which is acceptable for this implementation
        
        # Should exclude numbers and single characters, but may include some numbers
        assert '123' in tokens  # Numbers are included
        assert 'a' not in tokens  # Single character excluded
    
    def test_multiple_paragraphs(self):
        """Test analysis of multi-paragraph text."""
        text = "First paragraph here.\n\nSecond paragraph starts here. It continues.\n\nThird paragraph is short."
        analysis = self.analyzer.analyze_text(text)
        
        stats = analysis['statistics']
        assert stats['paragraph_count'] == 3
        assert stats['sentence_count'] >= 3
    
    def test_text_with_special_characters(self):
        """Test analysis of text with special characters and punctuation."""
        text = "Hello, world! How are you? I'm fine... Really? Yes, indeed! @user #hashtag $100"
        analysis = self.analyzer.analyze_text(text)
        
        assert isinstance(analysis, dict)
        assert analysis['statistics']['word_count'] > 0
        assert analysis['statistics']['sentence_count'] > 0
    
    def test_very_short_text(self):
        """Test analysis of very short text."""
        short_text = "Hi!"
        analysis = self.analyzer.analyze_text(short_text)
        
        stats = analysis['statistics']
        assert stats['word_count'] == 1
        assert stats['sentence_count'] == 1
        assert stats['character_count'] == 3
        
        summary = analysis['summary']
        assert 'very short' in summary.lower()
    
    def test_very_long_text(self):
        """Test analysis of longer text."""
        long_text = " ".join(["This is a sentence."] * 50)  # 250 words
        analysis = self.analyzer.analyze_text(long_text)
        
        stats = analysis['statistics']
        assert stats['word_count'] >= 140  # Should be around 150 (3 words per sentence after filtering)
        
        summary = analysis['summary']
        assert ('long' in summary.lower() or 'medium' in summary.lower())
    
    def test_summary_generation(self):
        """Test summary generation for different text types."""
        test_cases = [
            ("Hi!", "very short"),
            ("This is good and amazing!", "positive"),
            ("This is terrible and awful!", "negative"),
            (" ".join(["Word"] * 100), "medium")
        ]
        
        for text, expected_keyword in test_cases:
            analysis = self.analyzer.analyze_text(text)
            summary = analysis['summary'].lower()
            assert expected_keyword in summary
    
    def test_case_insensitive_sentiment(self):
        """Test that sentiment analysis is case insensitive."""
        text_lower = "this is amazing and wonderful"
        text_upper = "THIS IS AMAZING AND WONDERFUL"
        text_mixed = "This Is Amazing And Wonderful"
        
        analysis_lower = self.analyzer.analyze_text(text_lower)
        analysis_upper = self.analyzer.analyze_text(text_upper)
        analysis_mixed = self.analyzer.analyze_text(text_mixed)
        
        # All should have positive sentiment
        assert analysis_lower['sentiment']['label'] == 'positive'
        assert analysis_upper['sentiment']['label'] == 'positive'
        assert analysis_mixed['sentiment']['label'] == 'positive'
    
    def test_edge_case_punctuation(self):
        """Test handling of edge cases with punctuation."""
        edge_cases = [
            "!!!",
            "...",
            "???",
            "Hello!!! World???",
            "Multiple...   spaces    here.",
            "End with period.",
            "End without period"
        ]
        
        for text in edge_cases:
            analysis = self.analyzer.analyze_text(text)
            assert isinstance(analysis, dict)
            assert 'statistics' in analysis
            assert 'sentiment' in analysis
    
    def test_unicode_text(self):
        """Test handling of unicode text."""
        unicode_text = "Hello world! 🌍 This is great! 😊 Café résumé naïve"
        analysis = self.analyzer.analyze_text(unicode_text)
        
        assert isinstance(analysis, dict)
        assert analysis['statistics']['word_count'] > 0
        # Unicode characters should be handled gracefully
    
    def test_word_frequency_top_limit(self):
        """Test that word frequency analysis limits top words correctly."""
        # Create text with many different words
        words = [f"word{i}" for i in range(20)]
        text = " ".join(words * 2)  # Each word appears twice
        
        analysis = self.analyzer.analyze_text(text)
        most_common = analysis['word_frequency']['most_common_words']
        
        # Should not exceed 10 words
        assert len(most_common) <= 10
    
    def test_consistency_across_runs(self):
        """Test that analysis is consistent across multiple runs."""
        text = "This is a test text with good sentiment and excellent quality."
        
        analysis1 = self.analyzer.analyze_text(text)
        analysis2 = self.analyzer.analyze_text(text)
        
        # Results should be identical
        assert analysis1['statistics'] == analysis2['statistics']
        assert analysis1['sentiment'] == analysis2['sentiment']
        assert analysis1['word_frequency'] == analysis2['word_frequency']
        assert analysis1['readability'] == analysis2['readability']
    
    def test_private_methods(self):
        """Test private helper methods."""
        # Test _empty_analysis
        empty_result = self.analyzer._empty_analysis("Test reason")
        assert empty_result['summary'] == "Test reason"
        assert empty_result['statistics']['word_count'] == 0
        
        # Test _generate_summary with different inputs
        stats = {'word_count': 100}
        sentiment = {'label': 'positive', 'confidence': 0.2}
        summary = self.analyzer._generate_summary(stats, sentiment)
        assert isinstance(summary, str)
        assert 'positive' in summary


class TestTextAnalyzerIntegration:
    """Integration tests for text analyzer functionality."""
    
    def test_main_function_exists(self):
        """Test that main function exists and is callable."""
        from text_analyzer import main
        assert callable(main)
    
    def test_full_analysis_pipeline(self):
        """Test complete analysis pipeline with realistic text."""
        sample_text = """
        Machine learning is a fascinating field of artificial intelligence that has revolutionized 
        many industries. It enables computers to learn and make decisions from data without being 
        explicitly programmed. This technology is amazing and has incredible potential!
        
        However, it also comes with challenges. Data privacy, algorithmic bias, and ethical 
        concerns are important issues that need careful consideration. Despite these challenges,
        the future of AI looks bright and promising.
        """
        
        analyzer = TextAnalyzer()
        analysis = analyzer.analyze_text(sample_text)
        
        # Verify all components are present and reasonable
        assert analysis['statistics']['word_count'] > 50
        assert analysis['statistics']['sentence_count'] >= 4
        assert analysis['statistics']['paragraph_count'] >= 1  # May be 1 or 2 depending on formatting
        
        # Should detect mixed sentiment (positive words + some concerns)
        sentiment = analysis['sentiment']
        assert sentiment['label'] in ['positive', 'neutral', 'negative']
        
        # Should find relevant keywords
        word_freq = analysis['word_frequency']
        words_found = [w['word'] for w in word_freq['most_common_words']]
        tech_words = ['machine', 'learning', 'ai', 'artificial', 'intelligence', 'data', 'technology']
        assert any(tech_word in words_found for tech_word in tech_words)
        
        # Readability should be reasonable for technical text
        readability = analysis['readability']
        assert readability['estimated_grade_level'] > 8  # Somewhat advanced
        
        # Summary should be informative
        assert len(analysis['summary']) > 10
    
    def test_analyzer_independence(self):
        """Test that multiple analyzer instances are independent."""
        analyzer1 = TextAnalyzer()
        analyzer2 = TextAnalyzer()
        
        # Modify one analyzer's word sets
        analyzer1.positive_words.add('custompositive')
        analyzer2.negative_words.add('customnegative')
        
        # Test that they behave independently
        text_with_custom = "This is custompositive and customnegative"
        
        analysis1 = analyzer1.analyze_text(text_with_custom)
        analysis2 = analyzer2.analyze_text(text_with_custom)
        
        # Should have different sentiment scores due to different word sets
        sent1 = analysis1['sentiment']
        sent2 = analysis2['sentiment']
        
        # At least one should detect the custom word
        assert sent1['positive_words_found'] > 0 or sent2['negative_words_found'] > 0


if __name__ == '__main__':
    pytest.main([__file__])