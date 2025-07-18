"""
Unit tests for PIC criteria data model.

Tests cover initialization, validation, serialization, and edge cases
following software development best practices.
"""

import pytest
from src.data.models.pic import PICCriteria


class TestPICCriteria:
    """Test suite for PICCriteria class."""
    
    def test_valid_pic_creation(self):
        """Test creating PIC criteria with valid inputs."""
        # Arrange
        population = "Adults with Type 2 diabetes"
        intervention = "Metformin therapy"
        comparator = "Placebo or standard care"
        
        # Act
        pic = PICCriteria(
            population=population,
            intervention=intervention,
            comparator=comparator
        )
        
        # Assert
        assert pic.population == population
        assert pic.intervention == intervention
        assert pic.comparator == comparator
    
    def test_empty_population_raises_error(self):
        """Test that empty population raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Population criteria cannot be empty"):
            PICCriteria(
                population="",
                intervention="Metformin therapy",
                comparator="Placebo"
            )
    
    def test_whitespace_only_population_raises_error(self):
        """Test that whitespace-only population raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Population criteria cannot be empty"):
            PICCriteria(
                population="   ",
                intervention="Metformin therapy",
                comparator="Placebo"
            )
    
    def test_empty_intervention_raises_error(self):
        """Test that empty intervention raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Intervention criteria cannot be empty"):
            PICCriteria(
                population="Adults with diabetes",
                intervention="",
                comparator="Placebo"
            )
    
    def test_empty_comparator_raises_error(self):
        """Test that empty comparator raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Comparator criteria cannot be empty"):
            PICCriteria(
                population="Adults with diabetes",
                intervention="Metformin therapy",
                comparator=""
            )
    
    def test_to_dict_conversion(self):
        """Test conversion of PIC criteria to dictionary."""
        # Arrange
        pic = PICCriteria(
            population="Adults with Type 2 diabetes",
            intervention="Metformin therapy",
            comparator="Placebo or standard care"
        )
        
        # Act
        result = pic.to_dict()
        
        # Assert
        expected = {
            'population': "Adults with Type 2 diabetes",
            'intervention': "Metformin therapy",
            'comparator': "Placebo or standard care"
        }
        assert result == expected
        assert isinstance(result, dict)
    
    def test_from_dict_creation(self):
        """Test creating PIC criteria from dictionary."""
        # Arrange
        data = {
            'population': "Adults with Type 2 diabetes",
            'intervention': "Metformin therapy",
            'comparator': "Placebo or standard care"
        }
        
        # Act
        pic = PICCriteria.from_dict(data)
        
        # Assert
        assert pic.population == data['population']
        assert pic.intervention == data['intervention']
        assert pic.comparator == data['comparator']
    
    def test_from_dict_with_empty_values_raises_error(self):
        """Test that from_dict with empty values raises ValueError."""
        # Arrange
        data = {
            'population': "",
            'intervention': "Metformin therapy",
            'comparator': "Placebo"
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Population criteria cannot be empty"):
            PICCriteria.from_dict(data)
    
    def test_from_dict_with_missing_keys_raises_error(self):
        """Test that from_dict with missing keys raises KeyError."""
        # Arrange
        data = {
            'population': "Adults with diabetes",
            'intervention': "Metformin therapy"
            # Missing 'comparator' key
        }
        
        # Act & Assert
        with pytest.raises(KeyError):
            PICCriteria.from_dict(data)
    
    def test_str_representation(self):
        """Test string representation of PIC criteria."""
        # Arrange
        pic = PICCriteria(
            population="Adults with Type 2 diabetes",
            intervention="Metformin therapy",
            comparator="Placebo or standard care"
        )
        
        # Act
        result = str(pic)
        
        # Assert
        expected = ("Population: Adults with Type 2 diabetes\n"
                   "Intervention: Metformin therapy\n"
                   "Comparator: Placebo or standard care")
        assert result == expected
    
    def test_round_trip_serialization(self):
        """Test that to_dict and from_dict are inverse operations."""
        # Arrange
        original = PICCriteria(
            population="Adults with Type 2 diabetes",
            intervention="Metformin therapy",
            comparator="Placebo or standard care"
        )
        
        # Act
        dict_repr = original.to_dict()
        reconstructed = PICCriteria.from_dict(dict_repr)
        
        # Assert
        assert original.population == reconstructed.population
        assert original.intervention == reconstructed.intervention
        assert original.comparator == reconstructed.comparator
    
    def test_pic_with_special_characters(self):
        """Test PIC criteria with special characters and unicode."""
        # Arrange & Act
        pic = PICCriteria(
            population="Adults aged 18-65 with Type 2 diabetes (HbA1c ≥7%)",
            intervention="Metformin 500mg twice daily",
            comparator="Placebo or standard care (insulin/sulfonylurea)"
        )
        
        # Assert
        assert "≥" in pic.population
        assert "500mg" in pic.intervention
        assert "insulin/sulfonylurea" in pic.comparator
    
    def test_pic_with_leading_trailing_whitespace(self):
        """Test that leading/trailing whitespace is handled correctly."""
        # Arrange & Act
        pic = PICCriteria(
            population="  Adults with diabetes  ",
            intervention="  Metformin therapy  ",
            comparator="  Placebo  "
        )
        
        # Assert - Values should be stored with whitespace
        assert pic.population == "  Adults with diabetes  "
        assert pic.intervention == "  Metformin therapy  "
        assert pic.comparator == "  Placebo  "
    
    def test_pic_equality(self):
        """Test equality comparison between PIC criteria objects."""
        # Arrange
        pic1 = PICCriteria(
            population="Adults with diabetes",
            intervention="Metformin",
            comparator="Placebo"
        )
        pic2 = PICCriteria(
            population="Adults with diabetes",
            intervention="Metformin",
            comparator="Placebo"
        )
        pic3 = PICCriteria(
            population="Adults with diabetes",
            intervention="Insulin",
            comparator="Placebo"
        )
        
        # Act & Assert
        assert pic1 == pic2
        assert pic1 != pic3
    
    def test_pic_hash_consistency(self):
        """Test that identical PIC criteria have same hash."""
        # Arrange
        pic1 = PICCriteria(
            population="Adults with diabetes",
            intervention="Metformin",
            comparator="Placebo"
        )
        pic2 = PICCriteria(
            population="Adults with diabetes",
            intervention="Metformin",
            comparator="Placebo"
        )
        
        # Act & Assert
        assert hash(pic1) == hash(pic2)
    
    def test_pic_with_very_long_strings(self):
        """Test PIC criteria with very long strings."""
        # Arrange
        long_population = "A" * 1000
        long_intervention = "B" * 1000
        long_comparator = "C" * 1000
        
        # Act
        pic = PICCriteria(
            population=long_population,
            intervention=long_intervention,
            comparator=long_comparator
        )
        
        # Assert
        assert len(pic.population) == 1000
        assert len(pic.intervention) == 1000
        assert len(pic.comparator) == 1000


class TestPICCriteriaEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_pic_with_none_values_raises_error(self):
        """Test that None values raise appropriate errors."""
        # Test population as None
        with pytest.raises(AttributeError):
            PICCriteria(
                population=None,
                intervention="Metformin",
                comparator="Placebo"
            )
    
    def test_pic_with_numeric_strings(self):
        """Test PIC criteria with numeric strings."""
        # Arrange & Act
        pic = PICCriteria(
            population="123 participants",
            intervention="456mg dosage",
            comparator="789 control group"
        )
        
        # Assert
        assert pic.population == "123 participants"
        assert pic.intervention == "456mg dosage"
        assert pic.comparator == "789 control group"
    
    def test_pic_with_multiline_strings(self):
        """Test PIC criteria with multiline strings."""
        # Arrange & Act
        pic = PICCriteria(
            population="Adults with Type 2 diabetes\naged 18-65 years",
            intervention="Metformin therapy\n500mg twice daily",
            comparator="Placebo or standard care\nas control"
        )
        
        # Assert
        assert "\n" in pic.population
        assert "\n" in pic.intervention
        assert "\n" in pic.comparator