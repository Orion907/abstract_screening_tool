"""
Screening Engine

Main orchestrator that coordinates the entire screening process.
Simplified for demo with essential screening workflow and basic progress tracking.
"""

from typing import List, Dict, Any, Optional, Callable
import time

from ..data.models import PICCriteria, Abstract, ScreeningResult, ScreeningDecision
from ..data.processors import CSVProcessor, TextCleaner
from ..llm import PromptGenerator, ResponseParser, OpenAIClient


class ScreeningEngine:
    """
    Main orchestrator for the abstract screening process.
    
    Demo version focuses on core functionality with basic error handling
    and progress tracking.
    """
    
    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        Initialize the screening engine.
        
        Args:
            api_key: API key for LLM provider
            model_name: Name of the LLM model to use
        """
        self.csv_processor = CSVProcessor()
        self.text_cleaner = TextCleaner()
        self.prompt_generator = PromptGenerator()
        self.response_parser = ResponseParser()
        self.llm_client = OpenAIClient(api_key, model_name)
        
        # Demo configuration
        self.max_retries = 3
        self.retry_delay = 1.0
    
    def process_screening_batch(self, 
                               pic_criteria: PICCriteria,
                               abstracts: List[Abstract],
                               progress_callback: Optional[Callable[[int, int], None]] = None) -> List[ScreeningResult]:
        """
        Main entry point for screening a batch of abstracts.
        
        Args:
            pic_criteria: The PIC criteria for screening
            abstracts: List of abstracts to screen
            progress_callback: Optional callback for progress updates (current, total)
            
        Returns:
            List[ScreeningResult]: Screening results for all abstracts
        """
        results = []
        total_abstracts = len(abstracts)
        
        for i, abstract in enumerate(abstracts):
            try:
                # Clean the abstract text
                cleaned_abstract = self._prepare_abstract_for_screening(abstract)
                
                # Generate screening prompt
                prompt = self.prompt_generator.generate_screening_prompt(
                    pic_criteria, 
                    cleaned_abstract
                )
                
                # Execute screening with retry logic
                result = self._execute_screening_with_retry(
                    abstract.reference_id,
                    prompt
                )
                
                results.append(result)
                
                # Update progress
                if progress_callback:
                    progress_callback(i + 1, total_abstracts)
                
                # Small delay to avoid overwhelming the API
                time.sleep(0.1)
                
            except Exception as e:
                # Create error result for failed processing
                error_result = ScreeningResult.create_error_result(
                    abstract.reference_id,
                    f"Screening failed: {str(e)}"
                )
                results.append(error_result)
                
                # Update progress even on error
                if progress_callback:
                    progress_callback(i + 1, total_abstracts)
        
        return results
    
    def _prepare_abstract_for_screening(self, abstract: Abstract) -> Abstract:
        """
        Prepare abstract for screening by cleaning text.
        
        Args:
            abstract: Original abstract
            
        Returns:
            Abstract: Abstract with cleaned text
        """
        cleaned_title = self.text_cleaner.clean_title(abstract.title)
        cleaned_abstract_text = self.text_cleaner.clean_abstract_text(abstract.abstract_text)
        
        return Abstract(
            reference_id=abstract.reference_id,
            title=cleaned_title,
            abstract_text=cleaned_abstract_text,
            ground_truth=abstract.ground_truth
        )
    
    def _execute_screening_with_retry(self, reference_id: str, prompt: str) -> ScreeningResult:
        """
        Execute screening with retry logic for API failures.
        
        Args:
            reference_id: Reference ID for the abstract
            prompt: Generated screening prompt
            
        Returns:
            ScreeningResult: Screening result
        """
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                # Make LLM API call
                response = self.llm_client.generate_response(
                    prompt=prompt,
                    max_tokens=500,
                    temperature=0.1
                )
                
                if response['success']:
                    # Parse response into screening result
                    result = self.response_parser.parse_screening_response(
                        response['response'],
                        reference_id
                    )
                    return result
                else:
                    last_error = response.get('error', 'Unknown API error')
                    
            except Exception as e:
                last_error = str(e)
            
            # Wait before retry (exponential backoff)
            if attempt < self.max_retries - 1:
                time.sleep(self.retry_delay * (2 ** attempt))
        
        # All retries failed
        return ScreeningResult.create_error_result(
            reference_id,
            f"Max retries exceeded. Last error: {last_error}"
        )
    
    def validate_setup(self) -> Dict[str, Any]:
        """
        Validate that the screening engine is properly configured.
        
        Returns:
            Dict containing validation results
        """
        validation_results = {
            'valid': True,
            'issues': []
        }
        
        # Test LLM connection
        try:
            if not self.llm_client.test_connection():
                validation_results['valid'] = False
                validation_results['issues'].append("LLM API connection failed")
        except Exception as e:
            validation_results['valid'] = False
            validation_results['issues'].append(f"LLM API error: {str(e)}")
        
        # Validate prompt generator
        try:
            test_pic = PICCriteria(
                population="Test population",
                intervention="Test intervention", 
                comparator="Test comparator"
            )
            test_abstract = Abstract(
                reference_id="TEST001",
                title="Test title",
                abstract_text="Test abstract text"
            )
            
            prompt = self.prompt_generator.generate_screening_prompt(test_pic, test_abstract)
            
            if not self.prompt_generator.validate_prompt_length(prompt):
                validation_results['issues'].append("Generated prompt exceeds token limits")
                
        except Exception as e:
            validation_results['valid'] = False
            validation_results['issues'].append(f"Prompt generation error: {str(e)}")
        
        return validation_results
    
    def get_screening_stats(self, results: List[ScreeningResult]) -> Dict[str, Any]:
        """
        Calculate screening statistics from results.
        
        Args:
            results: List of screening results
            
        Returns:
            Dict containing screening statistics
        """
        if not results:
            return {
                'total_processed': 0,
                'included': 0,
                'excluded': 0,
                'errors': 0,
                'inclusion_rate': 0.0,
                'error_rate': 0.0
            }
        
        total = len(results)
        included = sum(1 for r in results if r.is_included())
        excluded = sum(1 for r in results if r.is_excluded())
        errors = sum(1 for r in results if r.decision == ScreeningDecision.ERROR)
        
        return {
            'total_processed': total,
            'included': included,
            'excluded': excluded,
            'errors': errors,
            'inclusion_rate': (included / total) * 100 if total > 0 else 0.0,
            'error_rate': (errors / total) * 100 if total > 0 else 0.0
        }
    
    def compare_with_ground_truth(self, results: List[ScreeningResult], 
                                 abstracts: List[Abstract]) -> Dict[str, Any]:
        """
        Compare screening results with ground truth decisions.
        
        Args:
            results: AI screening results
            abstracts: Original abstracts with ground truth
            
        Returns:
            Dict containing comparison metrics
        """
        # Create lookup for ground truth
        ground_truth_lookup = {
            abstract.reference_id: abstract.ground_truth 
            for abstract in abstracts 
            if abstract.ground_truth
        }
        
        if not ground_truth_lookup:
            return {
                'has_ground_truth': False,
                'message': 'No ground truth data available for comparison'
            }
        
        # Calculate agreement metrics
        total_compared = 0
        agreements = 0
        
        for result in results:
            if result.reference_id in ground_truth_lookup:
                ground_truth = ground_truth_lookup[result.reference_id]
                ai_decision = result.decision.value
                
                if ground_truth.lower() == ai_decision.lower():
                    agreements += 1
                
                total_compared += 1
        
        accuracy = (agreements / total_compared) * 100 if total_compared > 0 else 0.0
        
        return {
            'has_ground_truth': True,
            'total_compared': total_compared,
            'agreements': agreements,
            'accuracy_percentage': accuracy,
            'disagreements': total_compared - agreements
        }