"""
Data Models Package

This package contains the core data structures for the Abstract Screening Tool.
Simplified for demo implementation while maintaining extensibility.
"""

from .pic import PICCriteria
from .abstract import Abstract
from .screening import ScreeningResult, ScreeningDecision

__all__ = [
    'PICCriteria',
    'Abstract', 
    'ScreeningResult',
    'ScreeningDecision'
]