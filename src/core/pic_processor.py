"""
PIC Processor

Processes PIC criteria from user input into structured format.
Simplified for demo with basic parsing and validation.
"""

import re
from typing import Dict, List, Optional, Any

from ..data.models import PICCriteria


class PICProcessor:
    """
    Processes PIC criteria from user input into structured format.
    
    Demo version handles basic text parsing and validation.
    """
    
    def __init__(self):
        """Initialize PIC processor."""
        self.default_pic_examples = self._get_default_examples()
    
    def parse_pic_from_text(self, text: str) -> PICCriteria:
        """
        Parse PIC criteria from free-form text input.
        
        Args:
            text: Free-form text containing PIC criteria
            
        Returns:
            PICCriteria: Parsed PIC criteria
            
        Raises:
            ValueError: If PIC criteria cannot be parsed
        """
        if not text or not text.strip():
            raise ValueError("PIC criteria text cannot be empty")
        
        # Try to extract structured PIC components
        population = self._extract_component(text, "population")
        intervention = self._extract_component(text, "intervention")
        comparator = self._extract_component(text, "comparator")
        
        # Validate that all components were found
        if not population:
            raise ValueError("Could not identify Population criteria in text")
        if not intervention:
            raise ValueError("Could not identify Intervention criteria in text")
        if not comparator:
            raise ValueError("Could not identify Comparator criteria in text")
        
        return PICCriteria(
            population=population,
            intervention=intervention,
            comparator=comparator
        )
    
    def _extract_component(self, text: str, component_type: str) -> Optional[str]:
        """
        Extract a specific PIC component from text.
        
        Args:
            text: Input text
            component_type: Type of component (population, intervention, comparator)
            
        Returns:
            str: Extracted component text or None if not found
        """
        # Define patterns for each component type - order matters!
        patterns = {
            "population": [
                r"^\s*p\s*[:=]\s*([^\n\r]+)",  # Single letter first
                r"(?:population|participants?|subjects?|patients?)\s*:?\s*([^\n\r]+)",
                r"(?:study population|target population)\s*:?\s*([^\n\r]+)"
            ],
            "intervention": [
                r"^\s*i\s*[:=]\s*([^\n\r]+)",  # Single letter first
                r"(?:intervention|treatment|therapy|drug|medication)\s*:?\s*([^\n\r]+)",
                r"(?:experimental|active treatment)\s*:?\s*([^\n\r]+)"
            ],
            "comparator": [
                r"^\s*c\s*[:=]\s*([^\n\r]+)",  # Single letter first
                r"(?:comparator|comparison|control|placebo)\s*:?\s*([^\n\r]+)",
                r"(?:control group|standard care)\s*:?\s*([^\n\r]+)"
            ]
        }
        
        # Try each pattern for the component type
        for pattern in patterns.get(component_type, []):
            match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            if match:
                extracted = match.group(1).strip()
                # Clean up common artifacts
                extracted = re.sub(r'^[^\w\s]+', '', extracted)  # Remove leading punctuation
                extracted = re.sub(r'[^\w\s\.\)]+$', '', extracted)  # Remove trailing punctuation but keep periods and parentheses
                if extracted:
                    return extracted
        
        return None
    
    def validate_pic_completeness(self, pic_criteria: PICCriteria) -> Dict[str, Any]:
        """
        Validate that PIC criteria are complete and reasonable.
        
        Args:
            pic_criteria: PIC criteria to validate
            
        Returns:
            Dict containing validation results
        """
        validation_results = {
            'valid': True,
            'issues': [],
            'warnings': []
        }
        
        # Check minimum length requirements
        if len(pic_criteria.population.strip()) < 5:
            validation_results['warnings'].append("Population criteria seems very short")
        
        if len(pic_criteria.intervention.strip()) < 5:
            validation_results['warnings'].append("Intervention criteria seems very short")
        
        if len(pic_criteria.comparator.strip()) < 5:
            validation_results['warnings'].append("Comparator criteria seems very short")
        
        # Check for overly generic terms
        generic_terms = ['any', 'all', 'various', 'different', 'multiple']
        
        for term in generic_terms:
            if term.lower() in pic_criteria.population.lower():
                validation_results['warnings'].append(f"Population contains generic term: '{term}'")
            if term.lower() in pic_criteria.intervention.lower():
                validation_results['warnings'].append(f"Intervention contains generic term: '{term}'")
            if term.lower() in pic_criteria.comparator.lower():
                validation_results['warnings'].append(f"Comparator contains generic term: '{term}'")
        
        # Check for reasonable length limits
        if len(pic_criteria.population) > 200:
            validation_results['warnings'].append("Population criteria is very long")
        
        if len(pic_criteria.intervention) > 200:
            validation_results['warnings'].append("Intervention criteria is very long")
        
        if len(pic_criteria.comparator) > 200:
            validation_results['warnings'].append("Comparator criteria is very long")
        
        return validation_results
    
    def standardize_pic_format(self, pic_criteria: PICCriteria) -> PICCriteria:
        """
        Standardize PIC criteria format for consistency.
        
        Args:
            pic_criteria: Original PIC criteria
            
        Returns:
            PICCriteria: Standardized PIC criteria
        """
        # Clean and standardize each component
        population = self._standardize_component(pic_criteria.population)
        intervention = self._standardize_component(pic_criteria.intervention)
        comparator = self._standardize_component(pic_criteria.comparator)
        
        return PICCriteria(
            population=population,
            intervention=intervention,
            comparator=comparator
        )
    
    def _standardize_component(self, component: str) -> str:
        """
        Standardize a single PIC component.
        
        Args:
            component: Component text to standardize
            
        Returns:
            str: Standardized component text
        """
        # Remove extra whitespace
        standardized = re.sub(r'\s+', ' ', component.strip())
        
        # Ensure proper capitalization
        standardized = standardized[0].upper() + standardized[1:] if standardized else ""
        
        # Remove trailing punctuation except periods
        standardized = re.sub(r'[!?;,]+$', '', standardized)
        
        return standardized
    
    def get_pic_suggestions(self, partial_text: str) -> List[str]:
        """
        Get suggestions for PIC criteria based on partial text.
        
        Args:
            partial_text: Partial text input
            
        Returns:
            List[str]: List of suggested completions
        """
        suggestions = []
        
        # Check if any default examples match
        for example in self.default_pic_examples:
            if any(keyword in partial_text.lower() for keyword in example['keywords']):
                suggestions.append(example['template'])
        
        # Limit to top 3 suggestions
        return suggestions[:3]
    
    def _get_default_examples(self) -> List[Dict]:
        """
        Get default PIC criteria examples for common research areas.
        
        Returns:
            List[Dict]: List of example PIC criteria with keywords
        """
        return [
            {
                'keywords': ['diabetes', 'metformin', 'blood sugar', 'glucose'],
                'template': 'Population: Adults with Type 2 diabetes\nIntervention: Metformin therapy\nComparator: Placebo or standard care'
            },
            {
                'keywords': ['hypertension', 'blood pressure', 'ACE inhibitor'],
                'template': 'Population: Adults with hypertension\nIntervention: ACE inhibitor therapy\nComparator: Placebo or other antihypertensive drugs'
            },
            {
                'keywords': ['depression', 'antidepressant', 'therapy'],
                'template': 'Population: Adults with major depressive disorder\nIntervention: Cognitive behavioral therapy\nComparator: Standard care or medication'
            },
            {
                'keywords': ['cancer', 'chemotherapy', 'oncology'],
                'template': 'Population: Adults with cancer\nIntervention: Chemotherapy treatment\nComparator: Standard care or alternative treatments'
            },
            {
                'keywords': ['pain', 'analgesic', 'chronic pain'],
                'template': 'Population: Adults with chronic pain\nIntervention: Analgesic medication\nComparator: Placebo or alternative pain management'
            }
        ]
    
    def create_pic_template(self) -> str:
        """
        Create a blank PIC template for user input.
        
        Returns:
            str: PIC template with placeholders
        """
        return """Population: [Describe the target population - e.g., adults with specific condition]

Intervention: [Describe the intervention being studied - e.g., specific treatment or therapy]

Comparator: [Describe what the intervention is compared to - e.g., placebo, standard care, alternative treatment]"""