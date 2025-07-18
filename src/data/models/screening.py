"""
Screening Results Data Model

This module defines the data structure for storing screening decisions
and their reasoning. Simplified for demo implementation.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class ScreeningDecision(Enum):
    """
    Enumeration of possible screening decisions.
    """
    INCLUDE = "Include"
    EXCLUDE = "Exclude"
    ERROR = "Error"


@dataclass
class ScreeningResult:
    """
    Represents the result of screening a single abstract.
    
    Simplified for demo with basic Include/Exclude decisions and reasoning.
    """
    
    reference_id: str
    decision: ScreeningDecision
    reasoning: str
    confidence: Optional[float] = None  # For future use
    
    def __post_init__(self):
        """
        Basic validation for demo purposes.
        Ensures required fields are not empty.
        """
        if not self.reference_id.strip():
            raise ValueError("Reference ID cannot be empty")
        if not self.reasoning.strip():
            raise ValueError("Reasoning cannot be empty")
    
    def to_dict(self) -> dict:
        """
        Convert screening result to dictionary format.
        
        Returns:
            dict: Dictionary representation of screening result
        """
        return {
            'reference_id': self.reference_id,
            'decision': self.decision.value,
            'reasoning': self.reasoning,
            'confidence': self.confidence
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ScreeningResult':
        """
        Create screening result from dictionary data.
        
        Args:
            data: Dictionary containing screening result fields
            
        Returns:
            ScreeningResult: Initialized screening result object
        """
        return cls(
            reference_id=data['reference_id'],
            decision=ScreeningDecision(data['decision']),
            reasoning=data['reasoning'],
            confidence=data.get('confidence')
        )
    
    @classmethod
    def create_error_result(cls, reference_id: str, error_message: str) -> 'ScreeningResult':
        """
        Create an error result for failed processing.
        
        Args:
            reference_id: The reference ID that failed
            error_message: Description of the error
            
        Returns:
            ScreeningResult: Error result object
        """
        return cls(
            reference_id=reference_id,
            decision=ScreeningDecision.ERROR,
            reasoning=f"Processing failed: {error_message}"
        )
    
    def is_included(self) -> bool:
        """
        Check if the screening decision is to include the abstract.
        
        Returns:
            bool: True if decision is Include, False otherwise
        """
        return self.decision == ScreeningDecision.INCLUDE
    
    def is_excluded(self) -> bool:
        """
        Check if the screening decision is to exclude the abstract.
        
        Returns:
            bool: True if decision is Exclude, False otherwise
        """
        return self.decision == ScreeningDecision.EXCLUDE
    
    def __str__(self) -> str:
        """
        String representation for display and debugging.
        
        Returns:
            str: Formatted screening result string
        """
        return f"ID: {self.reference_id} | Decision: {self.decision.value} | Reasoning: {self.reasoning[:100]}..."