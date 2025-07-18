"""
LLM Integration Package

This package handles Large Language Model interactions for abstract screening.
Simplified for demo implementation.
"""

from .prompt_generator import PromptGenerator
from .response_parser import ResponseParser
from .api_clients import BaseLLMClient, OpenAIClient

__all__ = [
    'PromptGenerator',
    'ResponseParser',
    'BaseLLMClient',
    'OpenAIClient'
]