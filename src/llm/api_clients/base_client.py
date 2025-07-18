"""
Base LLM API Client

This module defines the abstract base class for LLM API clients.
Provides common interface for different LLM providers.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseLLMClient(ABC):
    """
    Abstract base class for LLM API clients.
    
    Defines the common interface that all LLM clients must implement.
    """
    
    def __init__(self, api_key: str, model_name: str):
        """
        Initialize the LLM client.
        
        Args:
            api_key: API key for the LLM provider
            model_name: Name of the model to use
        """
        self.api_key = api_key
        self.model_name = model_name
    
    @abstractmethod
    def generate_response(self, prompt: str, max_tokens: int = 1000, 
                         temperature: float = 0.1) -> Dict[str, Any]:
        """
        Generate a response from the LLM.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            temperature: Temperature for response generation
            
        Returns:
            Dict containing response text and metadata
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test if the API connection is working.
        
        Returns:
            bool: True if connection is successful
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dict containing model information
        """
        return {
            'provider': self.__class__.__name__,
            'model_name': self.model_name
        }