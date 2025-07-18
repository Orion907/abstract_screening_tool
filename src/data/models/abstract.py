"""
Abstract Data Model

This module defines the data structure for storing research abstracts
and their metadata. Simplified for demo implementation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Abstract:
    """
    Represents a research abstract with its metadata.
    
    Simplified for demo with fixed field structure matching the known CSV format.
    """
    
    reference_id: str
    title: str
    abstract_text: str
    ground_truth: Optional[str] = None  # For demo comparison with expert decisions
    
    def __post_init__(self):
        """
        Basic validation for demo purposes.
        Ensures required fields are not empty.
        """
        if not self.reference_id.strip():
            raise ValueError("Reference ID cannot be empty")
        if not self.title.strip():
            raise ValueError("Title cannot be empty") 
        if not self.abstract_text.strip():
            raise ValueError("Abstract text cannot be empty")
    
    def to_dict(self) -> dict:
        """
        Convert abstract to dictionary format for easy serialization.
        
        Returns:
            dict: Dictionary representation of abstract
        """
        return {
            'reference_id': self.reference_id,
            'title': self.title,
            'abstract_text': self.abstract_text,
            'ground_truth': self.ground_truth
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Abstract':
        """
        Create abstract from dictionary data.
        
        Args:
            data: Dictionary containing abstract fields
            
        Returns:
            Abstract: Initialized abstract object
        """
        return cls(
            reference_id=data['reference_id'],
            title=data['title'],
            abstract_text=data['abstract_text'],
            ground_truth=data.get('ground_truth')
        )
    
    def get_combined_text(self) -> str:
        """
        Get title and abstract combined for LLM processing.
        
        Returns:
            str: Combined title and abstract text
        """
        return f"Title: {self.title}\n\nAbstract: {self.abstract_text}"
    
    def __str__(self) -> str:
        """
        String representation for display and debugging.
        
        Returns:
            str: Formatted abstract string
        """
        return f"ID: {self.reference_id}\nTitle: {self.title[:100]}...\nAbstract: {self.abstract_text[:200]}..."