"""
OpenAI API Client

This module provides OpenAI API integration for the demo implementation.
Simplified with basic retry logic and error handling.
"""

import json
import time
from typing import Dict, Any, Optional

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .base_client import BaseLLMClient


class OpenAIClient(BaseLLMClient):
    """
    OpenAI API client for LLM interactions.
    
    Demo version with basic functionality and error handling.
    """
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI client.
        
        Args:
            api_key: OpenAI API key
            model_name: Model name (default: gpt-3.5-turbo)
        """
        super().__init__(api_key, model_name)
        
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Run: pip install openai")
        
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_response(self, prompt: str, max_tokens: int = 1000, 
                         temperature: float = 0.1) -> Dict[str, Any]:
        """
        Generate response from OpenAI API.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            temperature: Temperature for response generation
            
        Returns:
            Dict containing response and metadata
        """
        try:
            # Make API call with retry logic
            response = self._make_api_call_with_retry(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature
            )
            
            return {
                'response': response.choices[0].message.content,
                'model': response.model,
                'usage': {
                    'prompt_tokens': response.usage.prompt_tokens,
                    'completion_tokens': response.usage.completion_tokens,
                    'total_tokens': response.usage.total_tokens
                },
                'success': True
            }
            
        except Exception as e:
            return {
                'response': None,
                'error': str(e),
                'success': False
            }
    
    def _make_api_call_with_retry(self, prompt: str, max_tokens: int, 
                                 temperature: float, max_retries: int = 3) -> Any:
        """
        Make API call with retry logic.
        
        Args:
            prompt: The input prompt
            max_tokens: Maximum tokens in response
            temperature: Temperature for response generation
            max_retries: Maximum number of retries
            
        Returns:
            OpenAI API response
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": "You are a helpful research assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response
                
            except openai.RateLimitError as e:
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                    continue
                else:
                    raise e
            except Exception as e:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                else:
                    raise e
    
    def test_connection(self) -> bool:
        """
        Test OpenAI API connection.
        
        Returns:
            bool: True if connection successful
        """
        try:
            # Simple test call
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return True
            
        except Exception:
            return False
    
    def get_available_models(self) -> Dict[str, Any]:
        """
        Get list of available models.
        
        Returns:
            Dict containing available models
        """
        try:
            models = self.client.models.list()
            return {
                'models': [model.id for model in models.data],
                'success': True
            }
        except Exception as e:
            return {
                'models': [],
                'error': str(e),
                'success': False
            }