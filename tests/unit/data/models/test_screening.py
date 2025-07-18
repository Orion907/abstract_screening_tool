"""
Unit tests for Screening results data model.

Tests cover initialization, validation, serialization, and edge cases
following software development best practices.
"""

import pytest
from src.data.models.screening import ScreeningResult, ScreeningDecision


class TestScreeningDecision:
    """Test suite for ScreeningDecision enum."""
    
    def test_enum_values(self):
        """Test that enum has correct values."""
        # Act & Assert
        assert ScreeningDecision.INCLUDE.value == "Include"
        assert ScreeningDecision.EXCLUDE.value == "Exclude"
        assert ScreeningDecision.ERROR.value == "Error"
    
    def test_enum_equality(self):
        """Test enum equality comparisons."""
        # Act & Assert
        assert ScreeningDecision.INCLUDE == ScreeningDecision.INCLUDE
        assert ScreeningDecision.INCLUDE != ScreeningDecision.EXCLUDE
        assert ScreeningDecision.EXCLUDE != ScreeningDecision.ERROR


class TestScreeningResult:
    """Test suite for ScreeningResult class."""
    
    def test_valid_screening_result_creation(self):
        """Test creating ScreeningResult with valid inputs."""
        # Arrange
        reference_id = "REF001"
        decision = ScreeningDecision.INCLUDE
        reasoning = "Meets all inclusion criteria for population, intervention, and comparator"
        
        # Act
        result = ScreeningResult(
            reference_id=reference_id,
            decision=decision,
            reasoning=reasoning
        )
        
        # Assert
        assert result.reference_id == reference_id
        assert result.decision == decision
        assert result.reasoning == reasoning
        assert result.confidence is None
    
    def test_screening_result_with_confidence(self):
        """Test creating ScreeningResult with confidence score."""
        # Arrange
        reference_id = "REF001"
        decision = ScreeningDecision.INCLUDE
        reasoning = "Clear match for all criteria"
        confidence = 0.95
        
        # Act
        result = ScreeningResult(
            reference_id=reference_id,
            decision=decision,
            reasoning=reasoning,
            confidence=confidence
        )
        
        # Assert
        assert result.confidence == confidence
    
    def test_empty_reference_id_raises_error(self):
        """Test that empty reference ID raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Reference ID cannot be empty"):
            ScreeningResult(
                reference_id="",
                decision=ScreeningDecision.INCLUDE,
                reasoning="Test reasoning"
            )
    
    def test_whitespace_only_reference_id_raises_error(self):
        """Test that whitespace-only reference ID raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Reference ID cannot be empty"):
            ScreeningResult(
                reference_id="   ",
                decision=ScreeningDecision.INCLUDE,
                reasoning="Test reasoning"
            )
    
    def test_empty_reasoning_raises_error(self):
        """Test that empty reasoning raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Reasoning cannot be empty"):
            ScreeningResult(
                reference_id="REF001",
                decision=ScreeningDecision.INCLUDE,
                reasoning=""
            )
    
    def test_whitespace_only_reasoning_raises_error(self):
        """Test that whitespace-only reasoning raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Reasoning cannot be empty"):
            ScreeningResult(
                reference_id="REF001",
                decision=ScreeningDecision.INCLUDE,
                reasoning="   "
            )
    
    def test_to_dict_conversion(self):
        """Test conversion of ScreeningResult to dictionary."""
        # Arrange
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Meets all criteria",
            confidence=0.85
        )
        
        # Act
        dict_result = result.to_dict()
        
        # Assert
        expected = {
            'reference_id': "REF001",
            'decision': "Include",
            'reasoning': "Meets all criteria",
            'confidence': 0.85
        }
        assert dict_result == expected
        assert isinstance(dict_result, dict)
    
    def test_to_dict_without_confidence(self):
        """Test to_dict conversion without confidence."""
        # Arrange
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.EXCLUDE,
            reasoning="Does not meet population criteria"
        )
        
        # Act
        dict_result = result.to_dict()
        
        # Assert
        expected = {
            'reference_id': "REF001",
            'decision': "Exclude",
            'reasoning': "Does not meet population criteria",
            'confidence': None
        }
        assert dict_result == expected
    
    def test_from_dict_creation(self):
        """Test creating ScreeningResult from dictionary."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'decision': "Include",
            'reasoning': "Meets all criteria",
            'confidence': 0.85
        }
        
        # Act
        result = ScreeningResult.from_dict(data)
        
        # Assert
        assert result.reference_id == data['reference_id']
        assert result.decision == ScreeningDecision.INCLUDE
        assert result.reasoning == data['reasoning']
        assert result.confidence == data['confidence']
    
    def test_from_dict_without_confidence(self):
        """Test creating ScreeningResult from dictionary without confidence."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'decision': "Exclude",
            'reasoning': "Does not meet criteria"
        }
        
        # Act
        result = ScreeningResult.from_dict(data)
        
        # Assert
        assert result.reference_id == data['reference_id']
        assert result.decision == ScreeningDecision.EXCLUDE
        assert result.reasoning == data['reasoning']
        assert result.confidence is None
    
    def test_from_dict_with_empty_values_raises_error(self):
        """Test that from_dict with empty values raises ValueError."""
        # Arrange
        data = {
            'reference_id': "",
            'decision': "Include",
            'reasoning': "Test reasoning"
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Reference ID cannot be empty"):
            ScreeningResult.from_dict(data)
    
    def test_from_dict_with_invalid_decision_raises_error(self):
        """Test that from_dict with invalid decision raises ValueError."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'decision': "Invalid",
            'reasoning': "Test reasoning"
        }
        
        # Act & Assert
        with pytest.raises(ValueError):
            ScreeningResult.from_dict(data)
    
    def test_from_dict_with_missing_keys_raises_error(self):
        """Test that from_dict with missing keys raises KeyError."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'decision': "Include"
            # Missing 'reasoning' key
        }
        
        # Act & Assert
        with pytest.raises(KeyError):
            ScreeningResult.from_dict(data)
    
    def test_create_error_result(self):
        """Test creating error result."""
        # Arrange
        reference_id = "REF001"
        error_message = "API timeout occurred"
        
        # Act
        result = ScreeningResult.create_error_result(reference_id, error_message)
        
        # Assert
        assert result.reference_id == reference_id
        assert result.decision == ScreeningDecision.ERROR
        assert "Processing failed: API timeout occurred" in result.reasoning
    
    def test_is_included_method(self):
        """Test is_included method."""
        # Arrange
        include_result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Meets criteria"
        )
        exclude_result = ScreeningResult(
            reference_id="REF002",
            decision=ScreeningDecision.EXCLUDE,
            reasoning="Does not meet criteria"
        )
        error_result = ScreeningResult(
            reference_id="REF003",
            decision=ScreeningDecision.ERROR,
            reasoning="Processing failed"
        )
        
        # Act & Assert
        assert include_result.is_included() is True
        assert exclude_result.is_included() is False
        assert error_result.is_included() is False
    
    def test_is_excluded_method(self):
        """Test is_excluded method."""
        # Arrange
        include_result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Meets criteria"
        )
        exclude_result = ScreeningResult(
            reference_id="REF002",
            decision=ScreeningDecision.EXCLUDE,
            reasoning="Does not meet criteria"
        )
        error_result = ScreeningResult(
            reference_id="REF003",
            decision=ScreeningDecision.ERROR,
            reasoning="Processing failed"
        )
        
        # Act & Assert
        assert include_result.is_excluded() is False
        assert exclude_result.is_excluded() is True
        assert error_result.is_excluded() is False
    
    def test_str_representation(self):
        """Test string representation of ScreeningResult."""
        # Arrange
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="This is a very long reasoning text that should be truncated in the string representation for better readability and display purposes."
        )
        
        # Act
        str_result = str(result)
        
        # Assert
        assert "ID: REF001" in str_result
        assert "Decision: Include" in str_result
        assert "Reasoning:" in str_result
        assert "..." in str_result  # Should be truncated
    
    def test_round_trip_serialization(self):
        """Test that to_dict and from_dict are inverse operations."""
        # Arrange
        original = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.EXCLUDE,
            reasoning="Does not meet intervention criteria",
            confidence=0.75
        )
        
        # Act
        dict_repr = original.to_dict()
        reconstructed = ScreeningResult.from_dict(dict_repr)
        
        # Assert
        assert original.reference_id == reconstructed.reference_id
        assert original.decision == reconstructed.decision
        assert original.reasoning == reconstructed.reasoning
        assert original.confidence == reconstructed.confidence
    
    def test_screening_result_with_special_characters(self):
        """Test ScreeningResult with special characters and unicode."""
        # Arrange & Act
        result = ScreeningResult(
            reference_id="REF-001_α",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Population: adults with diabetes (HbA1c ≥7%). Intervention: metformin 500mg/day. Comparator: placebo (p<0.05)."
        )
        
        # Assert
        assert "α" in result.reference_id
        assert "≥" in result.reasoning
        assert "p<0.05" in result.reasoning
    
    def test_screening_result_with_very_long_strings(self):
        """Test ScreeningResult with very long strings."""
        # Arrange
        long_id = "A" * 100
        long_reasoning = "B" * 2000
        
        # Act
        result = ScreeningResult(
            reference_id=long_id,
            decision=ScreeningDecision.INCLUDE,
            reasoning=long_reasoning
        )
        
        # Assert
        assert len(result.reference_id) == 100
        assert len(result.reasoning) == 2000
    
    def test_screening_result_equality(self):
        """Test equality comparison between ScreeningResult objects."""
        # Arrange
        result1 = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Meets criteria",
            confidence=0.85
        )
        result2 = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Meets criteria",
            confidence=0.85
        )
        result3 = ScreeningResult(
            reference_id="REF002",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Meets criteria",
            confidence=0.85
        )
        
        # Act & Assert
        assert result1 == result2
        assert result1 != result3


class TestScreeningResultEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_screening_result_with_none_values_raises_error(self):
        """Test that None values raise appropriate errors."""
        # Test reference_id as None
        with pytest.raises(AttributeError):
            ScreeningResult(
                reference_id=None,
                decision=ScreeningDecision.INCLUDE,
                reasoning="Test reasoning"
            )
    
    def test_screening_result_with_multiline_reasoning(self):
        """Test ScreeningResult with multiline reasoning."""
        # Arrange & Act
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.EXCLUDE,
            reasoning="Exclusion criteria:\n1. Wrong population\n2. Intervention not matching\n3. No suitable comparator"
        )
        
        # Assert
        assert "\n" in result.reasoning
        assert "1. Wrong population" in result.reasoning
        assert "3. No suitable comparator" in result.reasoning
    
    def test_screening_result_with_zero_confidence(self):
        """Test ScreeningResult with zero confidence."""
        # Arrange & Act
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.ERROR,
            reasoning="Could not determine criteria match",
            confidence=0.0
        )
        
        # Assert
        assert result.confidence == 0.0
    
    def test_screening_result_with_negative_confidence(self):
        """Test ScreeningResult with negative confidence."""
        # Arrange & Act
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Test reasoning",
            confidence=-0.5
        )
        
        # Assert
        assert result.confidence == -0.5
    
    def test_screening_result_with_confidence_over_one(self):
        """Test ScreeningResult with confidence over 1.0."""
        # Arrange & Act
        result = ScreeningResult(
            reference_id="REF001",
            decision=ScreeningDecision.INCLUDE,
            reasoning="Test reasoning",
            confidence=1.5
        )
        
        # Assert
        assert result.confidence == 1.5
    
    def test_all_decision_types(self):
        """Test all decision types work correctly."""
        # Arrange & Act
        include_result = ScreeningResult("REF001", ScreeningDecision.INCLUDE, "Include reasoning")
        exclude_result = ScreeningResult("REF002", ScreeningDecision.EXCLUDE, "Exclude reasoning")
        error_result = ScreeningResult("REF003", ScreeningDecision.ERROR, "Error reasoning")
        
        # Assert
        assert include_result.is_included() and not include_result.is_excluded()
        assert exclude_result.is_excluded() and not exclude_result.is_included()
        assert not error_result.is_included() and not error_result.is_excluded()