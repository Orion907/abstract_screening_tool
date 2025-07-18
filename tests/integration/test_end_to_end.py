"""
End-to-End Integration Tests

These tests verify the complete workflow from PIC criteria input through
CSV processing to final results output using mocked LLM responses.
"""

import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

from src.core import ScreeningEngine, PICProcessor, BatchProcessor
from src.data.models import PICCriteria, Abstract, ScreeningResult, ScreeningDecision
from src.data.processors import CSVProcessor, TextCleaner
from src.llm import PromptGenerator, ResponseParser


class TestEndToEndWorkflow:
    """End-to-end integration tests for the complete screening workflow."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.sample_csv_path = Path(__file__).parent.parent / "fixtures" / "sample_abstracts.csv"
        self.pic_processor = PICProcessor()
        self.csv_processor = CSVProcessor()
        
    def test_complete_workflow_with_mocked_llm(self):
        """Test complete workflow from PIC input to results with mocked LLM."""
        
        # Step 1: Parse PIC criteria
        pic_text = """
        Population: Adults with Type 2 diabetes
        Intervention: Metformin therapy
        Comparator: Placebo or standard care
        """
        
        pic_criteria = self.pic_processor.parse_pic_from_text(pic_text)
        assert pic_criteria is not None
        assert "diabetes" in pic_criteria.population.lower()
        assert "metformin" in pic_criteria.intervention.lower()
        assert "placebo" in pic_criteria.comparator.lower()
        
        # Step 2: Load and validate CSV
        abstracts = self.csv_processor.load_abstracts_from_csv(str(self.sample_csv_path))
        assert len(abstracts) == 6
        assert all(isinstance(abstract, Abstract) for abstract in abstracts)
        
        # Step 3: Mock LLM responses for screening
        with patch('src.llm.api_clients.OpenAIClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            
            # Mock responses for each abstract
            mock_responses = [
                {'success': True, 'response': '{"decision": "Include", "reasoning": "Study examines metformin in type 2 diabetes patients vs placebo"}'},
                {'success': True, 'response': '{"decision": "Exclude", "reasoning": "Study about surgical techniques, not diabetes or metformin"}'},
                {'success': True, 'response': '{"decision": "Include", "reasoning": "Metformin vs placebo trial in pre-diabetic adults"}'},
                {'success': True, 'response': '{"decision": "Exclude", "reasoning": "Coffee consumption study, not about diabetes medication"}'},
                {'success': True, 'response': '{"decision": "Include", "reasoning": "Metformin treatment study, though in PCOS patients"}'},
                {'success': True, 'response': '{"decision": "Exclude", "reasoning": "Social media study, not related to diabetes or metformin"}'}, 
            ]
            
            mock_client.generate_response.side_effect = mock_responses
            mock_client.test_connection.return_value = True
            
            # Step 4: Create screening engine and process
            screening_engine = ScreeningEngine("dummy_api_key", "gpt-3.5-turbo")
            
            # Process the abstracts
            results = screening_engine.process_screening_batch(pic_criteria, abstracts)
            
            # Step 5: Verify results
            assert len(results) == 6
            assert all(isinstance(result, ScreeningResult) for result in results)
            
            # Check that we got the expected decisions
            expected_decisions = ["Include", "Exclude", "Include", "Exclude", "Include", "Exclude"]
            actual_decisions = [result.decision.value for result in results]
            assert actual_decisions == expected_decisions
            
            # Verify LLM was called correctly
            assert mock_client.generate_response.call_count == 6
            
        # Step 6: Calculate accuracy against ground truth
        comparison = screening_engine.compare_with_ground_truth(results, abstracts)
        assert comparison['has_ground_truth'] is True
        assert comparison['total_compared'] == 6
        
        # Expected: 3 correct (REF001, REF002, REF004), 3 incorrect (REF003, REF005, REF006)
        expected_accuracy = 50.0  # 3/6 = 50%
        assert comparison['accuracy_percentage'] == expected_accuracy
        
    def test_csv_processing_integration(self):
        """Test CSV loading and processing integration."""
        
        # Load abstracts
        abstracts = self.csv_processor.load_abstracts_from_csv(str(self.sample_csv_path))
        
        # Verify abstracts loaded correctly
        assert len(abstracts) == 6
        
        # Check specific abstracts
        ref001 = next(a for a in abstracts if a.reference_id == "REF001")
        assert "metformin" in ref001.abstract_text.lower()
        assert "diabetes" in ref001.abstract_text.lower()
        assert ref001.ground_truth == "Include"
        
        ref002 = next(a for a in abstracts if a.reference_id == "REF002")
        assert "appendectomy" in ref002.abstract_text.lower()
        assert ref002.ground_truth == "Exclude"
        
        # Test CSV validation
        validation = self.csv_processor.validate_csv_file(str(self.sample_csv_path))
        assert validation['valid'] is True
        assert validation['missing_columns'] == []
        assert validation['total_rows'] == 6
        
    def test_text_cleaning_integration(self):
        """Test text cleaning integration with CSV processing."""
        
        # Load abstracts
        abstracts = self.csv_processor.load_abstracts_from_csv(str(self.sample_csv_path))
        
        # Clean text
        text_cleaner = TextCleaner()
        
        for abstract in abstracts:
            original_text = abstract.abstract_text
            cleaned_text = text_cleaner.clean_abstract_text(original_text)
            
            # Verify cleaning worked
            assert len(cleaned_text) > 0
            assert cleaned_text.strip() == cleaned_text  # No leading/trailing whitespace
            
            # Verify content is preserved
            assert len(cleaned_text) <= len(original_text)  # Should be same or shorter
            
    def test_prompt_generation_integration(self):
        """Test prompt generation integration with PIC processing."""
        
        # Parse PIC criteria
        pic_text = """
        Population: Adults with Type 2 diabetes
        Intervention: Metformin therapy  
        Comparator: Placebo or standard care
        """
        
        pic_criteria = self.pic_processor.parse_pic_from_text(pic_text)
        
        # Load sample abstract
        abstracts = self.csv_processor.load_abstracts_from_csv(str(self.sample_csv_path))
        test_abstract = abstracts[0]  # REF001
        
        # Generate prompt
        prompt_generator = PromptGenerator()
        prompt = prompt_generator.generate_screening_prompt(pic_criteria, test_abstract)
        
        # Verify prompt contains expected elements
        assert "diabetes" in prompt.lower()
        assert "metformin" in prompt.lower()
        assert "placebo" in prompt.lower()
        assert test_abstract.title in prompt
        assert test_abstract.abstract_text in prompt
        assert "JSON" in prompt  # Should request JSON response
        
        # Verify prompt length is reasonable
        assert len(prompt) > 500  # Should be substantial
        assert len(prompt) < 5000  # But not too long
        
    def test_response_parsing_integration(self):
        """Test response parsing integration."""
        
        response_parser = ResponseParser()
        
        # Test various response formats
        test_responses = [
            '{"decision": "Include", "reasoning": "Meets all criteria"}',
            '{"decision": "Exclude", "reasoning": "Wrong population"}',
            'Some text before {"decision": "Include", "reasoning": "Valid study"} some text after',
            '{"decision": "Error", "reasoning": "Could not determine"}',
        ]
        
        for i, response_text in enumerate(test_responses):
            result = response_parser.parse_screening_response(response_text, f"REF{i+1:03d}")
            
            assert isinstance(result, ScreeningResult)
            assert result.reference_id == f"REF{i+1:03d}"
            assert result.decision in [ScreeningDecision.INCLUDE, ScreeningDecision.EXCLUDE, ScreeningDecision.ERROR]
            assert len(result.reasoning) > 0
            
    def test_batch_processing_integration(self):
        """Test batch processing integration."""
        
        # Load abstracts
        abstracts = self.csv_processor.load_abstracts_from_csv(str(self.sample_csv_path))
        
        # Create batch processor
        batch_processor = BatchProcessor(batch_size=2, delay_between_batches=0.1)
        
        # Mock screening function
        def mock_screening_function(batch_abstracts):
            results = []
            for abstract in batch_abstracts:
                result = ScreeningResult(
                    reference_id=abstract.reference_id,
                    decision=ScreeningDecision.INCLUDE,
                    reasoning=f"Mock result for {abstract.reference_id}"
                )
                results.append(result)
            return results
        
        # Process in batches
        results = batch_processor.process_in_batches(
            abstracts, 
            mock_screening_function
        )
        
        # Verify results
        assert len(results) == 6
        assert all(isinstance(result, ScreeningResult) for result in results)
        
        # Check processing stats
        summary = batch_processor.get_processing_summary()
        assert summary['total_processed'] == 6
        assert summary['success_rate'] == 100.0
        
    def test_export_functionality_integration(self):
        """Test export functionality integration."""
        
        # Load abstracts
        abstracts = self.csv_processor.load_abstracts_from_csv(str(self.sample_csv_path))
        
        # Create mock results
        results = [
            ScreeningResult("REF001", ScreeningDecision.INCLUDE, "Meets criteria"),
            ScreeningResult("REF002", ScreeningDecision.EXCLUDE, "Wrong intervention"),
            ScreeningResult("REF003", ScreeningDecision.INCLUDE, "Suitable study"),
        ]
        
        # Test CSV export
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            tmp_path = tmp_file.name
        
        try:
            self.csv_processor.save_results_to_csv(abstracts[:3], 
                                                  [r.to_dict() for r in results], 
                                                  tmp_path)
            
            # Verify export
            exported_df = pd.read_csv(tmp_path)
            assert len(exported_df) == 3
            assert 'Reference ID' in exported_df.columns
            assert 'AI Decision' in exported_df.columns
            assert 'AI Reasoning' in exported_df.columns
            assert 'Manual Decision' in exported_df.columns
            
        finally:
            os.unlink(tmp_path)


class TestErrorHandlingIntegration:
    """Test error handling in integrated workflows."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.pic_processor = PICProcessor()
        self.csv_processor = CSVProcessor()
        
    def test_invalid_csv_handling(self):
        """Test handling of invalid CSV files."""
        
        # Create invalid CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_file:
            tmp_file.write("Wrong,Column,Names\n")
            tmp_file.write("REF001,Title,Abstract\n")
            tmp_path = tmp_file.name
        
        try:
            # Should raise error for missing columns
            with pytest.raises(ValueError, match="Missing required columns"):
                self.csv_processor.load_abstracts_from_csv(tmp_path)
                
        finally:
            os.unlink(tmp_path)
            
    def test_invalid_pic_criteria_handling(self):
        """Test handling of invalid PIC criteria."""
        
        # Test missing components
        invalid_pic_texts = [
            "Population: Adults with diabetes",  # Missing intervention and comparator
            "Intervention: Metformin therapy",   # Missing population and comparator
            "",                                  # Empty text
            "Random text with no PIC structure" # No recognizable format
        ]
        
        for invalid_text in invalid_pic_texts:
            with pytest.raises(ValueError):
                self.pic_processor.parse_pic_from_text(invalid_text)
                
    def test_llm_error_handling(self):
        """Test handling of LLM API errors."""
        
        # Load sample data
        sample_csv_path = Path(__file__).parent.parent / "fixtures" / "sample_abstracts.csv"
        abstracts = self.csv_processor.load_abstracts_from_csv(str(sample_csv_path))
        
        pic_criteria = PICCriteria(
            population="Adults with diabetes",
            intervention="Metformin therapy",
            comparator="Placebo"
        )
        
        # Mock LLM client to return errors
        with patch('src.llm.api_clients.OpenAIClient') as mock_client_class:
            mock_client = Mock()
            mock_client_class.return_value = mock_client
            
            # Mock API failures
            mock_client.generate_response.return_value = {
                'success': False,
                'error': 'API rate limit exceeded'
            }
            mock_client.test_connection.return_value = True
            
            # Create screening engine
            screening_engine = ScreeningEngine("dummy_api_key", "gpt-3.5-turbo")
            
            # Process should handle errors gracefully
            results = screening_engine.process_screening_batch(pic_criteria, abstracts[:2])
            
            # Should get error results
            assert len(results) == 2
            assert all(result.decision == ScreeningDecision.ERROR for result in results)
            assert all("Max retries exceeded" in result.reasoning for result in results)


class TestPerformanceIntegration:
    """Test performance aspects of integrated workflows."""
    
    def test_processing_time_reasonable(self):
        """Test that processing time is reasonable for demo purposes."""
        
        import time
        
        # Load sample data
        sample_csv_path = Path(__file__).parent.parent / "fixtures" / "sample_abstracts.csv"
        csv_processor = CSVProcessor()
        abstracts = csv_processor.load_abstracts_from_csv(str(sample_csv_path))
        
        # Measure CSV processing time
        start_time = time.time()
        validation = csv_processor.validate_csv_file(str(sample_csv_path))
        csv_time = time.time() - start_time
        
        # Should be very fast (< 1 second)
        assert csv_time < 1.0
        assert validation['valid'] is True
        
        # Measure PIC processing time
        pic_processor = PICProcessor()
        pic_text = """
        Population: Adults with Type 2 diabetes
        Intervention: Metformin therapy
        Comparator: Placebo or standard care
        """
        
        start_time = time.time()
        pic_criteria = pic_processor.parse_pic_from_text(pic_text)
        pic_time = time.time() - start_time
        
        # Should be very fast (< 0.1 seconds)
        assert pic_time < 0.1
        assert pic_criteria is not None
        
    def test_memory_usage_reasonable(self):
        """Test that memory usage is reasonable for demo purposes."""
        
        # Load sample data multiple times to test memory handling
        sample_csv_path = Path(__file__).parent.parent / "fixtures" / "sample_abstracts.csv"
        csv_processor = CSVProcessor()
        
        # Load abstracts multiple times
        all_abstracts = []
        for i in range(10):
            abstracts = csv_processor.load_abstracts_from_csv(str(sample_csv_path))
            all_abstracts.extend(abstracts)
        
        # Should handle multiple loads without issues
        assert len(all_abstracts) == 60  # 6 abstracts × 10 loads
        
        # Memory should be manageable (basic check)
        import sys
        memory_usage = sys.getsizeof(all_abstracts)
        assert memory_usage < 1000000  # Less than 1MB for demo data