"""
Response Parser

This module parses and validates LLM responses for abstract screening.
Simplified for demo with basic JSON parsing and validation.
"""

import json
import re
from typing import Dict, Any, Optional

from ..data.models import ScreeningResult, ScreeningDecision


class ResponseParser:
    """
    Parses LLM responses into structured screening results.
    
    Demo version handles JSON parsing with basic error recovery.
    """
    
    def __init__(self):
        """Initialize response parser."""
        pass
    
    def parse_screening_response(self, response_text: str, reference_id: str) -> ScreeningResult:
        """
        Parse LLM response into a ScreeningResult object.
        
        Args:
            response_text: Raw response text from LLM
            reference_id: Reference ID for the screened abstract
            
        Returns:
            ScreeningResult: Parsed screening result
        """
        try:
            # Try to parse JSON response
            parsed_response = self._extract_json_from_response(response_text)
            
            if parsed_response is None:
                return ScreeningResult.create_error_result(
                    reference_id, 
                    "Could not parse JSON response from LLM"
                )
            
            # Extract decision and reasoning
            decision = self._parse_decision(parsed_response.get('decision', ''))
            reasoning = parsed_response.get('reasoning', '').strip()
            
            if not reasoning:
                reasoning = "No reasoning provided"
            
            return ScreeningResult(
                reference_id=reference_id,
                decision=decision,
                reasoning=reasoning
            )
            
        except Exception as e:
            return ScreeningResult.create_error_result(
                reference_id,
                f"Error parsing response: {str(e)}"
            )
    
    def _extract_json_from_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """
        Extract JSON from response text, handling various formats.
        
        Args:
            response_text: Raw response text
            
        Returns:
            Dict containing parsed JSON or None if parsing fails
        """
        if not response_text:
            return None
        
        # Try direct JSON parsing first
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # Try to find JSON within the response
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group())
            except json.JSONDecodeError:
                pass
        
        # Try to extract decision and reasoning manually
        decision_match = re.search(r'"decision"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
        reasoning_match = re.search(r'"reasoning"\s*:\s*"([^"]+)"', response_text, re.IGNORECASE)
        
        if decision_match:
            return {
                'decision': decision_match.group(1),
                'reasoning': reasoning_match.group(1) if reasoning_match else "No reasoning provided"
            }
        
        return None
    
    def _parse_decision(self, decision_text: str) -> ScreeningDecision:
        """
        Parse decision text into ScreeningDecision enum.
        
        Args:
            decision_text: Decision text from LLM
            
        Returns:
            ScreeningDecision: Parsed decision
        """
        if not decision_text:
            return ScreeningDecision.ERROR
        
        decision_lower = decision_text.lower().strip()
        
        if 'include' in decision_lower:
            return ScreeningDecision.INCLUDE
        elif 'exclude' in decision_lower:
            return ScreeningDecision.EXCLUDE
        else:
            return ScreeningDecision.ERROR
    
    def validate_response_format(self, response_text: str) -> Dict[str, Any]:
        """
        Validate that response follows expected format.
        
        Args:
            response_text: Response text to validate
            
        Returns:
            Dict containing validation results
        """
        try:
            parsed = self._extract_json_from_response(response_text)
            
            if parsed is None:
                return {
                    'valid': False,
                    'error': 'Could not parse JSON from response'
                }
            
            # Check required fields
            required_fields = ['decision', 'reasoning']
            missing_fields = [field for field in required_fields if field not in parsed]
            
            if missing_fields:
                return {
                    'valid': False,
                    'error': f'Missing required fields: {missing_fields}'
                }
            
            # Validate decision value
            decision = parsed.get('decision', '').lower()
            if decision not in ['include', 'exclude']:
                return {
                    'valid': False,
                    'error': f'Invalid decision value: {decision}'
                }
            
            return {
                'valid': True,
                'parsed': parsed
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }