"""
Unit tests for CSV processor.

Tests cover file loading, validation, and error handling
following software development best practices.
"""

import pytest
import pandas as pd
import tempfile
import os
from unittest.mock import patch, MagicMock

from src.data.processors.csv_processor import CSVProcessor
from src.data.models.abstract import Abstract


class TestCSVProcessor:
    """Test suite for CSVProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = CSVProcessor()
    
    def test_initialization(self):
        """Test CSVProcessor initialization."""
        # Act & Assert
        assert self.processor.EXPECTED_COLUMNS == {
            'Reference ID': 'reference_id',
            'Title': 'title', 
            'Abstract': 'abstract_text',
            'Manual Decision': 'ground_truth'
        }
    
    def test_load_abstracts_from_valid_csv(self):
        """Test loading abstracts from valid CSV file."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract,Manual Decision\n")
            f.write("REF001,Test Study 1,This is abstract 1,Include\n")
            f.write("REF002,Test Study 2,This is abstract 2,Exclude\n")
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 2
            assert abstracts[0].reference_id == "REF001"
            assert abstracts[0].title == "Test Study 1"
            assert abstracts[0].abstract_text == "This is abstract 1"
            assert abstracts[0].ground_truth == "Include"
            assert abstracts[1].reference_id == "REF002"
            assert abstracts[1].ground_truth == "Exclude"
            
        finally:
            os.unlink(temp_path)
    
    def test_load_abstracts_without_ground_truth(self):
        """Test loading abstracts from CSV without ground truth column."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write("REF001,Test Study 1,This is abstract 1\n")
            f.write("REF002,Test Study 2,This is abstract 2\n")
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 2
            assert abstracts[0].ground_truth is None
            assert abstracts[1].ground_truth is None
            
        finally:
            os.unlink(temp_path)
    
    def test_load_abstracts_with_missing_columns_raises_error(self):
        """Test that missing required columns raises ValueError."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title\n")  # Missing Abstract column
            f.write("REF001,Test Study 1\n")
            temp_path = f.name
        
        try:
            # Act & Assert
            with pytest.raises(ValueError, match="Missing required columns"):
                self.processor.load_abstracts_from_csv(temp_path)
        finally:
            os.unlink(temp_path)
    
    def test_load_abstracts_with_invalid_file_raises_error(self):
        """Test that invalid file path raises FileNotFoundError."""
        # Act & Assert
        with pytest.raises(FileNotFoundError):
            self.processor.load_abstracts_from_csv("nonexistent_file.csv")
    
    def test_load_abstracts_with_empty_rows_skipped(self):
        """Test that rows with empty required fields are skipped."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write("REF001,Test Study 1,This is abstract 1\n")
            f.write(",Test Study 2,This is abstract 2\n")  # Empty reference ID
            f.write("REF003,Test Study 3,This is abstract 3\n")
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 2  # Row with empty reference ID skipped
            assert abstracts[0].reference_id == "REF001"
            assert abstracts[1].reference_id == "REF003"
            
        finally:
            os.unlink(temp_path)
    
    def test_validate_csv_columns_with_valid_columns(self):
        """Test CSV column validation with valid columns."""
        # Arrange
        df = pd.DataFrame({
            'Reference ID': ['REF001'],
            'Title': ['Test'],
            'Abstract': ['Test abstract'],
            'Manual Decision': ['Include']
        })
        
        # Act & Assert - Should not raise exception
        self.processor._validate_csv_columns(df)
    
    def test_validate_csv_columns_with_missing_columns(self):
        """Test CSV column validation with missing columns."""
        # Arrange
        df = pd.DataFrame({
            'Reference ID': ['REF001'],
            'Title': ['Test']
            # Missing Abstract column
        })
        
        # Act & Assert
        with pytest.raises(ValueError, match="Missing required columns"):
            self.processor._validate_csv_columns(df)
    
    def test_save_results_to_csv(self):
        """Test saving screening results to CSV."""
        # Arrange
        abstracts = [
            Abstract("REF001", "Test Study 1", "Abstract 1", "Include"),
            Abstract("REF002", "Test Study 2", "Abstract 2", "Exclude")
        ]
        results = [
            {'reference_id': 'REF001', 'decision': 'Include', 'reasoning': 'Meets criteria'},
            {'reference_id': 'REF002', 'decision': 'Exclude', 'reasoning': 'Wrong population'}
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            # Act
            self.processor.save_results_to_csv(abstracts, results, temp_path)
            
            # Assert
            df = pd.read_csv(temp_path)
            assert len(df) == 2
            assert 'Reference ID' in df.columns
            assert 'AI Decision' in df.columns
            assert 'AI Reasoning' in df.columns
            assert 'Manual Decision' in df.columns
            assert df.iloc[0]['AI Decision'] == 'Include'
            assert df.iloc[1]['AI Decision'] == 'Exclude'
            
        finally:
            os.unlink(temp_path)
    
    def test_save_results_with_missing_results(self):
        """Test saving results when some abstracts have no results."""
        # Arrange
        abstracts = [
            Abstract("REF001", "Test Study 1", "Abstract 1"),
            Abstract("REF002", "Test Study 2", "Abstract 2")
        ]
        results = [
            {'reference_id': 'REF001', 'decision': 'Include', 'reasoning': 'Meets criteria'}
            # Missing result for REF002
        ]
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_path = f.name
        
        try:
            # Act
            self.processor.save_results_to_csv(abstracts, results, temp_path)
            
            # Assert
            df = pd.read_csv(temp_path)
            assert len(df) == 2
            assert df.iloc[0]['AI Decision'] == 'Include'
            assert df.iloc[1]['AI Decision'] == 'Not Processed'
            assert df.iloc[1]['AI Reasoning'] == 'Not Processed'
            
        finally:
            os.unlink(temp_path)
    
    def test_get_csv_info_with_valid_file(self):
        """Test getting CSV file information."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract,Manual Decision\n")
            f.write("REF001,Test Study 1,Abstract 1,Include\n")
            f.write("REF002,Test Study 2,Abstract 2,Exclude\n")
            temp_path = f.name
        
        try:
            # Act
            info = self.processor.get_csv_info(temp_path)
            
            # Assert
            assert info['total_rows'] == 2
            assert 'Reference ID' in info['columns']
            assert 'Title' in info['columns']
            assert 'Abstract' in info['columns']
            assert info['has_ground_truth'] is True
            assert len(info['sample_titles']) == 2
            assert 'Test Study 1' in info['sample_titles']
            
        finally:
            os.unlink(temp_path)
    
    def test_get_csv_info_with_invalid_file(self):
        """Test getting CSV info with invalid file."""
        # Act
        info = self.processor.get_csv_info("nonexistent_file.csv")
        
        # Assert
        assert 'error' in info
    
    def test_validate_csv_file_with_valid_file(self):
        """Test validating a valid CSV file."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write("REF001,Test Study 1,Abstract 1\n")
            f.write("REF002,Test Study 2,Abstract 2\n")
            temp_path = f.name
        
        try:
            # Act
            validation = self.processor.validate_csv_file(temp_path)
            
            # Assert
            assert validation['valid'] is True
            assert validation['missing_columns'] == []
            assert validation['total_rows'] == 2
            assert validation['empty_rows'] == 0
            assert validation['missing_reference_ids'] == 0
            assert validation['missing_abstracts'] == 0
            
        finally:
            os.unlink(temp_path)
    
    def test_validate_csv_file_with_problems(self):
        """Test validating CSV file with various problems."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title\n")  # Missing Abstract column
            f.write("REF001,Test Study 1\n")
            f.write(",Test Study 2\n")  # Missing reference ID
            temp_path = f.name
        
        try:
            # Act
            validation = self.processor.validate_csv_file(temp_path)
            
            # Assert
            assert validation['valid'] is False
            assert 'Abstract' in validation['missing_columns']
            assert validation['total_rows'] == 2
            assert validation['missing_reference_ids'] == 1
            
        finally:
            os.unlink(temp_path)
    
    def test_validate_csv_file_with_invalid_file(self):
        """Test validating invalid file."""
        # Act
        validation = self.processor.validate_csv_file("nonexistent_file.csv")
        
        # Assert
        assert validation['valid'] is False
        assert 'error' in validation


class TestCSVProcessorEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = CSVProcessor()
    
    def test_load_abstracts_with_special_characters(self):
        """Test loading abstracts with special characters."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write("REF-001_α,Study with β-blockers,Abstract with special chars: ≥7% (p<0.05)\n")
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 1
            assert "α" in abstracts[0].reference_id
            assert "β-blockers" in abstracts[0].title
            assert "≥7%" in abstracts[0].abstract_text
            
        finally:
            os.unlink(temp_path)
    
    def test_load_abstracts_with_very_long_text(self):
        """Test loading abstracts with very long text."""
        # Arrange
        long_abstract = "A" * 5000
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write(f"REF001,Test Study,{long_abstract}\n")
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 1
            assert len(abstracts[0].abstract_text) == 5000
            
        finally:
            os.unlink(temp_path)
    
    def test_load_abstracts_with_commas_in_text(self):
        """Test loading abstracts with commas in text fields."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write('REF001,"Study with, commas in title","Abstract with, multiple, commas"\n')
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 1
            assert "commas in title" in abstracts[0].title
            assert "multiple, commas" in abstracts[0].abstract_text
            
        finally:
            os.unlink(temp_path)
    
    def test_load_abstracts_with_newlines_in_text(self):
        """Test loading abstracts with newlines in text fields."""
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Reference ID,Title,Abstract\n")
            f.write('REF001,"Multi-line\nTitle","Multi-line\nAbstract\nText"\n')
            temp_path = f.name
        
        try:
            # Act
            abstracts = self.processor.load_abstracts_from_csv(temp_path)
            
            # Assert
            assert len(abstracts) == 1
            assert "\n" in abstracts[0].title
            assert "\n" in abstracts[0].abstract_text
            
        finally:
            os.unlink(temp_path)
    
    def test_save_results_with_invalid_path_raises_error(self):
        """Test saving results with invalid path."""
        # Arrange
        abstracts = [Abstract("REF001", "Test", "Abstract")]
        results = [{'reference_id': 'REF001', 'decision': 'Include', 'reasoning': 'Test'}]
        
        # Act & Assert
        with pytest.raises(ValueError, match="Error saving results to CSV"):
            self.processor.save_results_to_csv(abstracts, results, "/invalid/path/file.csv")