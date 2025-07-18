"""
Text Cleaner

This module provides text cleaning and normalization utilities for abstract text.
Simplified for demo implementation with basic cleaning operations.
"""

import re
from typing import str


class TextCleaner:
    """
    Handles text cleaning and normalization for research abstracts.
    
    Demo version provides basic cleaning sufficient for LLM processing.
    """
    
    def __init__(self):
        """Initialize text cleaner with demo configuration."""
        pass
    
    def clean_abstract_text(self, text: str) -> str:
        """
        Clean and normalize abstract text for LLM processing.
        
        Args:
            text: Raw abstract text
            
        Returns:
            str: Cleaned abstract text
        """
        if not text or not isinstance(text, str):
            return ""
        
        # Start with the original text
        cleaned = text
        
        # Remove excessive whitespace
        cleaned = self._normalize_whitespace(cleaned)
        
        # Remove common artifacts from PDF extraction
        cleaned = self._remove_pdf_artifacts(cleaned)
        
        # Normalize punctuation
        cleaned = self._normalize_punctuation(cleaned)
        
        # Remove empty lines and extra spaces
        cleaned = self._remove_empty_lines(cleaned)
        
        return cleaned.strip()
    
    def clean_title(self, title: str) -> str:
        """
        Clean and normalize title text.
        
        Args:
            title: Raw title text
            
        Returns:
            str: Cleaned title text
        """
        if not title or not isinstance(title, str):
            return ""
        
        # Basic title cleaning
        cleaned = title.strip()
        
        # Remove excessive whitespace
        cleaned = self._normalize_whitespace(cleaned)
        
        # Remove trailing periods if present
        cleaned = re.sub(r'\.$', '', cleaned)
        
        return cleaned
    
    def _normalize_whitespace(self, text: str) -> str:
        """
        Normalize whitespace in text.
        
        Args:
            text: Input text
            
        Returns:
            str: Text with normalized whitespace
        """
        # Replace multiple spaces with single space
        text = re.sub(r' +', ' ', text)
        
        # Replace tabs with spaces
        text = re.sub(r'\t', ' ', text)
        
        # Normalize line breaks
        text = re.sub(r'\r\n', '\n', text)
        text = re.sub(r'\r', '\n', text)
        
        return text
    
    def _remove_pdf_artifacts(self, text: str) -> str:
        """
        Remove common PDF extraction artifacts.
        
        Args:
            text: Input text
            
        Returns:
            str: Text with PDF artifacts removed
        """
        # Remove page breaks and form feeds
        text = re.sub(r'\f', ' ', text)
        
        # Remove excessive line breaks
        text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)
        
        # Remove hyphenation at line ends (common in PDF extractions)
        text = re.sub(r'-\s*\n\s*', '', text)
        
        return text
    
    def _normalize_punctuation(self, text: str) -> str:
        """
        Normalize punctuation in text.
        
        Args:
            text: Input text
            
        Returns:
            str: Text with normalized punctuation
        """
        # Normalize quotes
        text = re.sub(r'[""]', '"', text)
        text = re.sub(r'['']', "'", text)
        
        # Normalize dashes
        text = re.sub(r'[–—]', '-', text)
        
        # Remove excessive punctuation
        text = re.sub(r'\.{3,}', '...', text)
        text = re.sub(r'!{2,}', '!', text)
        text = re.sub(r'\?{2,}', '?', text)
        
        return text
    
    def _remove_empty_lines(self, text: str) -> str:
        """
        Remove empty lines and excessive line breaks.
        
        Args:
            text: Input text
            
        Returns:
            str: Text with empty lines removed
        """
        # Split into lines and remove empty ones
        lines = text.split('\n')
        non_empty_lines = [line.strip() for line in lines if line.strip()]
        
        return '\n'.join(non_empty_lines)
    
    def get_word_count(self, text: str) -> int:
        """
        Get word count of cleaned text.
        
        Args:
            text: Input text
            
        Returns:
            int: Word count
        """
        if not text:
            return 0
        
        # Simple word count based on spaces
        words = text.split()
        return len(words)
    
    def truncate_text(self, text: str, max_words: int = 500) -> str:
        """
        Truncate text to maximum word count for LLM processing.
        
        Args:
            text: Input text
            max_words: Maximum number of words
            
        Returns:
            str: Truncated text
        """
        if not text:
            return ""
        
        words = text.split()
        
        if len(words) <= max_words:
            return text
        
        # Truncate and add ellipsis
        truncated_words = words[:max_words]
        return ' '.join(truncated_words) + '...'