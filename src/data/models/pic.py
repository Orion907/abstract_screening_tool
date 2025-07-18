"""
PIC (Population, Intervention, Comparator) Criteria Data Model

This module defines the data structures for storing and validating PIC criteria
used in abstract screening. Simplified for demo implementation with basic validation.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class PICCriteria:
    """
    Represents the Population, Intervention, Comparator criteria for abstract screening.
    
    This is a simplified version for demo purposes that focuses on the core PIC components
    without complex validation or optional fields.
    """
    
    population: str
    intervention: str 
    comparator: str
    
    def __post_init__(self):
        """
        Basic validation to ensure no empty criteria.
        Demo version uses simple not-empty checks only.
        """
        if not self.population.strip():
            raise ValueError("Population criteria cannot be empty")
        if not self.intervention.strip():
            raise ValueError("Intervention criteria cannot be empty")
        if not self.comparator.strip():
            raise ValueError("Comparator criteria cannot be empty")
    
    def to_dict(self) -> dict:
        """
        Convert PIC criteria to dictionary format for easy serialization.
        
        Returns:
            dict: Dictionary representation of PIC criteria
        """
        return {
            'population': self.population,
            'intervention': self.intervention,
            'comparator': self.comparator
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'PICCriteria':
        """
        Create PIC criteria from dictionary data.
        
        Args:
            data: Dictionary containing PIC criteria fields
            
        Returns:
            PICCriteria: Initialized PIC criteria object
        """
        return cls(
            population=data['population'],
            intervention=data['intervention'],
            comparator=data['comparator']
        )
    
    def __str__(self) -> str:
        """
        String representation for display and debugging.
        
        Returns:
            str: Formatted PIC criteria string
        """
        return f"Population: {self.population}\nIntervention: {self.intervention}\nComparator: {self.comparator}"