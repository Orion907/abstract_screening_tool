"""
Unit tests for PIC processor.

Tests cover text parsing, validation, and standardization
following software development best practices.
"""

import pytest
from unittest.mock import patch, MagicMock

from src.core.pic_processor import PICProcessor
from src.data.models.pic import PICCriteria


class TestPICProcessor:
    """Test suite for PICProcessor class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = PICProcessor()
    
    def test_initialization(self):
        """Test PICProcessor initialization."""
        # Act & Assert
        assert self.processor is not None
        assert hasattr(self.processor, 'default_pic_examples')
        assert len(self.processor.default_pic_examples) > 0
    
    def test_parse_pic_from_text_with_valid_input(self):
        """Test parsing PIC criteria from valid text."""
        # Arrange
        text = """
        Population: Adults with Type 2 diabetes
        Intervention: Metformin therapy
        Comparator: Placebo or standard care
        """
        
        # Act
        result = self.processor.parse_pic_from_text(text)
        
        # Assert
        assert isinstance(result, PICCriteria)
        assert result.population == "Adults with Type 2 diabetes"
        assert result.intervention == "Metformin therapy"
        assert result.comparator == "Placebo or standard care"
    
    def test_parse_pic_from_text_with_alternative_format(self):
        """Test parsing PIC criteria with alternative format."""
        # Arrange
        text = """
        P: Adults with hypertension
        I: ACE inhibitor therapy
        C: Placebo
        """
        
        # Act
        result = self.processor.parse_pic_from_text(text)
        
        # Assert
        assert result.population == "Adults with hypertension"
        assert result.intervention == "ACE inhibitor therapy"
        assert result.comparator == "Placebo"
    
    def test_parse_pic_from_text_with_mixed_case(self):
        """Test parsing PIC criteria with mixed case."""
        # Arrange
        text = """
        POPULATION: Adults with depression
        intervention: Cognitive behavioral therapy
        Comparator: Standard care
        """
        
        # Act
        result = self.processor.parse_pic_from_text(text)
        
        # Assert
        assert result.population == "Adults with depression"
        assert result.intervention == "Cognitive behavioral therapy"
        assert result.comparator == "Standard care"
    
    def test_parse_pic_from_text_with_empty_text_raises_error(self):
        """Test that empty text raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="PIC criteria text cannot be empty"):
            self.processor.parse_pic_from_text("")
    
    def test_parse_pic_from_text_with_missing_population_raises_error(self):
        """Test that missing population raises ValueError."""
        # Arrange
        text = """
        Intervention: Metformin therapy
        Comparator: Placebo
        """
        
        # Act & Assert
        with pytest.raises(ValueError, match="Could not identify Population criteria"):
            self.processor.parse_pic_from_text(text)
    
    def test_parse_pic_from_text_with_missing_intervention_raises_error(self):
        """Test that missing intervention raises ValueError."""
        # Arrange
        text = """
        Population: Adults with diabetes
        Comparator: Placebo
        """
        
        # Act & Assert
        with pytest.raises(ValueError, match="Could not identify Intervention criteria"):
            self.processor.parse_pic_from_text(text)
    
    def test_parse_pic_from_text_with_missing_comparator_raises_error(self):
        """Test that missing comparator raises ValueError."""
        # Arrange
        text = """
        Population: Adults with diabetes
        Intervention: Metformin therapy
        """
        
        # Act & Assert
        with pytest.raises(ValueError, match="Could not identify Comparator criteria"):
            self.processor.parse_pic_from_text(text)
    
    def test_extract_component_with_valid_pattern(self):
        """Test extracting component with valid pattern."""
        # Arrange
        text = "Population: Adults with Type 2 diabetes"
        
        # Act
        result = self.processor._extract_component(text, "population")
        
        # Assert
        assert result == "Adults with Type 2 diabetes"
    
    def test_extract_component_with_colon_format(self):
        """Test extracting component with colon format."""
        # Arrange
        text = "Intervention: Metformin 500mg twice daily"
        
        # Act
        result = self.processor._extract_component(text, "intervention")
        
        # Assert
        assert result == "Metformin 500mg twice daily"
    
    def test_extract_component_with_equals_format(self):
        """Test extracting component with equals format."""
        # Arrange
        text = "P = Adults with hypertension"
        
        # Act
        result = self.processor._extract_component(text, "population")
        
        # Assert
        assert result == "Adults with hypertension"
    
    def test_extract_component_with_no_match_returns_none(self):
        """Test extracting component with no match returns None."""
        # Arrange
        text = "This text contains no valid PIC patterns"
        
        # Act
        result = self.processor._extract_component(text, "population")
        
        # Assert
        assert result is None
    
    def test_validate_pic_completeness_with_valid_criteria(self):
        """Test validating complete PIC criteria."""
        # Arrange
        pic_criteria = PICCriteria(
            population="Adults with Type 2 diabetes mellitus",
            intervention="Metformin therapy 500mg twice daily",
            comparator="Placebo or standard care without metformin"
        )
        
        # Act
        result = self.processor.validate_pic_completeness(pic_criteria)
        
        # Assert
        assert result['valid'] is True
        assert len(result['issues']) == 0
    
    def test_validate_pic_completeness_with_short_criteria(self):
        """Test validating PIC criteria with short text."""
        # Arrange
        pic_criteria = PICCriteria(
            population="A",  # 1 char - short
            intervention="B",  # 1 char - short
            comparator="C"   # 1 char - short
        )
        
        # Act
        result = self.processor.validate_pic_completeness(pic_criteria)
        
        # Assert
        assert result['valid'] is True  # Still valid but has warnings
        assert len(result['warnings']) == 3  # All three are short
        assert "very short" in result['warnings'][0]
    
    def test_validate_pic_completeness_with_generic_terms(self):
        """Test validating PIC criteria with generic terms."""
        # Arrange
        pic_criteria = PICCriteria(
            population="Any adults with various conditions",
            intervention="Different treatments",
            comparator="Multiple control groups"
        )
        
        # Act
        result = self.processor.validate_pic_completeness(pic_criteria)
        
        # Assert
        assert len(result['warnings']) >= 3  # Should warn about generic terms
        assert any("generic term" in warning for warning in result['warnings'])
    
    def test_validate_pic_completeness_with_long_criteria(self):
        """Test validating PIC criteria with very long text."""
        # Arrange
        long_text = "A" * 250
        pic_criteria = PICCriteria(
            population=long_text,
            intervention=long_text,
            comparator=long_text
        )
        
        # Act
        result = self.processor.validate_pic_completeness(pic_criteria)
        
        # Assert
        assert len(result['warnings']) >= 3  # Should warn about long text
        assert any("very long" in warning for warning in result['warnings'])
    
    def test_standardize_pic_format(self):
        """Test standardizing PIC criteria format."""
        # Arrange
        pic_criteria = PICCriteria(
            population="  adults with diabetes  ",
            intervention="metformin therapy!!!",
            comparator="placebo or standard care???"
        )
        
        # Act
        result = self.processor.standardize_pic_format(pic_criteria)
        
        # Assert
        assert result.population == "Adults with diabetes"
        assert result.intervention == "Metformin therapy"
        assert result.comparator == "Placebo or standard care"
    
    def test_standardize_component(self):
        """Test standardizing a single component."""
        # Arrange
        component = "  adults   with   diabetes!!!  "
        
        # Act
        result = self.processor._standardize_component(component)
        
        # Assert
        assert result == "Adults with diabetes"
    
    def test_standardize_component_with_period(self):
        """Test standardizing component preserves periods."""
        # Arrange
        component = "adults with diabetes mellitus."
        
        # Act
        result = self.processor._standardize_component(component)
        
        # Assert
        assert result == "Adults with diabetes mellitus."
    
    def test_get_pic_suggestions_with_matching_keyword(self):
        """Test getting PIC suggestions with matching keyword."""
        # Arrange
        partial_text = "diabetes metformin"
        
        # Act
        suggestions = self.processor.get_pic_suggestions(partial_text)
        
        # Assert
        assert len(suggestions) > 0
        assert any("diabetes" in suggestion.lower() for suggestion in suggestions)
    
    def test_get_pic_suggestions_with_no_matching_keyword(self):
        """Test getting PIC suggestions with no matching keyword."""
        # Arrange
        partial_text = "random unrelated text"
        
        # Act
        suggestions = self.processor.get_pic_suggestions(partial_text)
        
        # Assert
        assert len(suggestions) == 0
    
    def test_get_pic_suggestions_limits_results(self):
        """Test that suggestions are limited to maximum number."""
        # Arrange
        partial_text = "therapy treatment medication"  # Should match multiple
        
        # Act
        suggestions = self.processor.get_pic_suggestions(partial_text)
        
        # Assert
        assert len(suggestions) <= 3  # Should be limited to 3
    
    def test_create_pic_template(self):
        """Test creating PIC template."""
        # Act
        template = self.processor.create_pic_template()
        
        # Assert
        assert "Population:" in template
        assert "Intervention:" in template
        assert "Comparator:" in template
        assert "[Describe" in template
    
    def test_get_default_examples_structure(self):
        """Test structure of default examples."""
        # Act
        examples = self.processor._get_default_examples()
        
        # Assert
        assert len(examples) > 0
        for example in examples:
            assert 'keywords' in example
            assert 'template' in example
            assert isinstance(example['keywords'], list)
            assert isinstance(example['template'], str)
            assert len(example['keywords']) > 0
            assert len(example['template']) > 0


class TestPICProcessorEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.processor = PICProcessor()
    
    def test_parse_pic_with_special_characters(self):
        """Test parsing PIC criteria with special characters."""
        # Arrange
        text = """
        Population: Adults with Type 2 diabetes (HbA1c ≥7%)
        Intervention: Metformin 500mg/day
        Comparator: Placebo (matched tablets)
        """
        
        # Act
        result = self.processor.parse_pic_from_text(text)
        
        # Assert
        assert "≥7%" in result.population
        assert "500mg/day" in result.intervention
        assert "(matched tablets)" in result.comparator
    
    def test_parse_pic_with_multiline_components(self):
        """Test parsing PIC criteria with multiline components."""
        # Arrange
        text = """
        Population: Adults with Type 2 diabetes
        aged 18-65 years
        Intervention: Metformin therapy
        any dose or formulation
        Comparator: Placebo or standard care
        """
        
        # Act
        result = self.processor.parse_pic_from_text(text)
        
        # Assert
        assert result.population == "Adults with Type 2 diabetes"
        assert result.intervention == "Metformin therapy"
        assert result.comparator == "Placebo or standard care"
    
    def test_parse_pic_with_punctuation_in_labels(self):
        """Test parsing PIC criteria with punctuation in labels."""
        # Arrange
        text = """
        Population: Adults with diabetes
        Intervention: Metformin therapy
        Comparator: Standard care
        """
        
        # Act
        result = self.processor.parse_pic_from_text(text)
        
        # Assert
        assert result.population == "Adults with diabetes"
        assert result.intervention == "Metformin therapy"
        assert result.comparator == "Standard care"
    
    def test_validate_pic_completeness_with_empty_criteria(self):
        """Test validation with minimal criteria."""
        # Arrange
        pic_criteria = PICCriteria(
            population="Test",
            intervention="Test",
            comparator="Test"
        )
        
        # Act
        result = self.processor.validate_pic_completeness(pic_criteria)
        
        # Assert
        assert result['valid'] is True
        assert len(result['warnings']) == 3  # All should be flagged as short
    
    def test_standardize_component_with_empty_string(self):
        """Test standardizing empty component."""
        # Arrange
        component = ""
        
        # Act
        result = self.processor._standardize_component(component)
        
        # Assert
        assert result == ""
    
    def test_standardize_component_with_only_whitespace(self):
        """Test standardizing whitespace-only component."""
        # Arrange
        component = "   \n\t  "
        
        # Act
        result = self.processor._standardize_component(component)
        
        # Assert
        assert result == ""