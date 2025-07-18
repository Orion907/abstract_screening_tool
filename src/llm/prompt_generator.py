"""
Prompt Generator

This module converts PIC criteria into optimized LLM prompts for abstract screening.
Simplified for demo with one well-tested prompt template.
"""

from typing import str
from ..data.models import PICCriteria, Abstract


class PromptGenerator:
    """
    Generates screening prompts for LLM based on PIC criteria.
    
    Demo version uses a single, well-tested prompt template.
    """
    
    def __init__(self):
        """Initialize prompt generator with demo template."""
        self.base_template = self._get_base_template()
    
    def generate_screening_prompt(self, pic_criteria: PICCriteria, abstract: Abstract) -> str:
        """
        Generate a screening prompt for a specific abstract and PIC criteria.
        
        Args:
            pic_criteria: The PIC criteria for screening
            abstract: The abstract to be screened
            
        Returns:
            str: Complete prompt for LLM screening
        """
        # Create the screening prompt
        prompt = self.base_template.format(
            population=pic_criteria.population,
            intervention=pic_criteria.intervention,
            comparator=pic_criteria.comparator,
            title=abstract.title,
            abstract_text=abstract.abstract_text
        )
        
        return prompt
    
    def _get_base_template(self) -> str:
        """
        Get the base prompt template for screening.
        
        Returns:
            str: Base prompt template
        """
        return """You are an expert systematic review researcher. Your task is to screen a research abstract to determine if it should be included in a systematic review based on specific criteria.

INCLUSION CRITERIA:
- Population: {population}
- Intervention: {intervention}
- Comparator: {comparator}

ABSTRACT TO SCREEN:
Title: {title}

Abstract: {abstract_text}

INSTRUCTIONS:
1. Carefully read the abstract and determine if it meets ALL inclusion criteria
2. The study must clearly involve the specified population, intervention, and comparator
3. If ANY criterion is not met, the abstract should be EXCLUDED
4. If ALL criteria are met, the abstract should be INCLUDED

RESPONSE FORMAT:
Provide your response in the following JSON format:
{{
    "decision": "Include" or "Exclude",
    "reasoning": "Brief explanation of your decision, specifically referencing which criteria were met or not met"
}}

Your response must be valid JSON only, with no additional text before or after."""
    
    def get_token_estimate(self, prompt: str) -> int:
        """
        Get rough estimate of tokens in prompt.
        
        Args:
            prompt: The prompt text
            
        Returns:
            int: Estimated token count
        """
        # Simple estimation: ~4 characters per token
        return len(prompt) // 4
    
    def validate_prompt_length(self, prompt: str, max_tokens: int = 4000) -> bool:
        """
        Validate that prompt is within token limits.
        
        Args:
            prompt: The prompt text
            max_tokens: Maximum allowed tokens
            
        Returns:
            bool: True if prompt is within limits
        """
        estimated_tokens = self.get_token_estimate(prompt)
        return estimated_tokens <= max_tokens