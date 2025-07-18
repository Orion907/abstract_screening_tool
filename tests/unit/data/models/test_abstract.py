"""
Unit tests for Abstract data model.

Tests cover initialization, validation, serialization, and edge cases
following software development best practices.
"""

import pytest
from src.data.models.abstract import Abstract


class TestAbstract:
    """Test suite for Abstract class."""
    
    def test_valid_abstract_creation(self):
        """Test creating Abstract with valid inputs."""
        # Arrange
        reference_id = "REF001"
        title = "Effects of Metformin on Type 2 Diabetes"
        abstract_text = "This study examines the effects of metformin therapy on patients with type 2 diabetes."
        
        # Act
        abstract = Abstract(
            reference_id=reference_id,
            title=title,
            abstract_text=abstract_text
        )
        
        # Assert
        assert abstract.reference_id == reference_id
        assert abstract.title == title
        assert abstract.abstract_text == abstract_text
        assert abstract.ground_truth is None
    
    def test_abstract_with_ground_truth(self):
        """Test creating Abstract with ground truth data."""
        # Arrange
        reference_id = "REF001"
        title = "Test Study"
        abstract_text = "Test abstract text"
        ground_truth = "Include"
        
        # Act
        abstract = Abstract(
            reference_id=reference_id,
            title=title,
            abstract_text=abstract_text,
            ground_truth=ground_truth
        )
        
        # Assert
        assert abstract.ground_truth == ground_truth
    
    def test_empty_reference_id_raises_error(self):
        """Test that empty reference ID raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Reference ID cannot be empty"):
            Abstract(
                reference_id="",
                title="Test Title",
                abstract_text="Test abstract"
            )
    
    def test_whitespace_only_reference_id_raises_error(self):
        """Test that whitespace-only reference ID raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Reference ID cannot be empty"):
            Abstract(
                reference_id="   ",
                title="Test Title",
                abstract_text="Test abstract"
            )
    
    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Abstract(
                reference_id="REF001",
                title="",
                abstract_text="Test abstract"
            )
    
    def test_empty_abstract_text_raises_error(self):
        """Test that empty abstract text raises ValueError."""
        # Arrange & Act & Assert
        with pytest.raises(ValueError, match="Abstract text cannot be empty"):
            Abstract(
                reference_id="REF001",
                title="Test Title",
                abstract_text=""
            )
    
    def test_to_dict_conversion(self):
        """Test conversion of Abstract to dictionary."""
        # Arrange
        abstract = Abstract(
            reference_id="REF001",
            title="Test Study",
            abstract_text="Test abstract text",
            ground_truth="Include"
        )
        
        # Act
        result = abstract.to_dict()
        
        # Assert
        expected = {
            'reference_id': "REF001",
            'title': "Test Study",
            'abstract_text': "Test abstract text",
            'ground_truth': "Include"
        }
        assert result == expected
        assert isinstance(result, dict)
    
    def test_to_dict_without_ground_truth(self):
        """Test to_dict conversion without ground truth."""
        # Arrange
        abstract = Abstract(
            reference_id="REF001",
            title="Test Study",
            abstract_text="Test abstract text"
        )
        
        # Act
        result = abstract.to_dict()
        
        # Assert
        expected = {
            'reference_id': "REF001",
            'title': "Test Study",
            'abstract_text': "Test abstract text",
            'ground_truth': None
        }
        assert result == expected
    
    def test_from_dict_creation(self):
        """Test creating Abstract from dictionary."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'title': "Test Study",
            'abstract_text': "Test abstract text",
            'ground_truth': "Include"
        }
        
        # Act
        abstract = Abstract.from_dict(data)
        
        # Assert
        assert abstract.reference_id == data['reference_id']
        assert abstract.title == data['title']
        assert abstract.abstract_text == data['abstract_text']
        assert abstract.ground_truth == data['ground_truth']
    
    def test_from_dict_without_ground_truth(self):
        """Test creating Abstract from dictionary without ground truth."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'title': "Test Study",
            'abstract_text': "Test abstract text"
        }
        
        # Act
        abstract = Abstract.from_dict(data)
        
        # Assert
        assert abstract.reference_id == data['reference_id']
        assert abstract.title == data['title']
        assert abstract.abstract_text == data['abstract_text']
        assert abstract.ground_truth is None
    
    def test_from_dict_with_empty_values_raises_error(self):
        """Test that from_dict with empty values raises ValueError."""
        # Arrange
        data = {
            'reference_id': "",
            'title': "Test Study",
            'abstract_text': "Test abstract text"
        }
        
        # Act & Assert
        with pytest.raises(ValueError, match="Reference ID cannot be empty"):
            Abstract.from_dict(data)
    
    def test_from_dict_with_missing_keys_raises_error(self):
        """Test that from_dict with missing keys raises KeyError."""
        # Arrange
        data = {
            'reference_id': "REF001",
            'title': "Test Study"
            # Missing 'abstract_text' key
        }
        
        # Act & Assert
        with pytest.raises(KeyError):
            Abstract.from_dict(data)
    
    def test_get_combined_text(self):
        """Test get_combined_text method."""
        # Arrange
        abstract = Abstract(
            reference_id="REF001",
            title="Test Study Title",
            abstract_text="This is the abstract text content."
        )
        
        # Act
        result = abstract.get_combined_text()
        
        # Assert
        expected = "Title: Test Study Title\n\nAbstract: This is the abstract text content."
        assert result == expected
    
    def test_str_representation(self):
        """Test string representation of Abstract."""
        # Arrange
        abstract = Abstract(
            reference_id="REF001",
            title="This is a very long title that should be truncated in the string representation for better readability",
            abstract_text="This is a very long abstract text that should also be truncated in the string representation to keep it manageable for display purposes and debugging."
        )
        
        # Act
        result = str(abstract)
        
        # Assert
        assert "ID: REF001" in result
        assert "Title:" in result
        assert "Abstract:" in result
        assert "..." in result  # Should be truncated
    
    def test_round_trip_serialization(self):
        """Test that to_dict and from_dict are inverse operations."""
        # Arrange
        original = Abstract(
            reference_id="REF001",
            title="Test Study",
            abstract_text="Test abstract text",
            ground_truth="Include"
        )
        
        # Act
        dict_repr = original.to_dict()
        reconstructed = Abstract.from_dict(dict_repr)
        
        # Assert
        assert original.reference_id == reconstructed.reference_id
        assert original.title == reconstructed.title
        assert original.abstract_text == reconstructed.abstract_text
        assert original.ground_truth == reconstructed.ground_truth
    
    def test_abstract_with_special_characters(self):
        """Test Abstract with special characters and unicode."""
        # Arrange & Act
        abstract = Abstract(
            reference_id="REF-001_α",
            title="Effects of β-blockers on cardiovascular outcomes (n=1,234)",
            abstract_text="This study examined the effects of β-blockers in patients with cardiovascular disease. Results showed significant improvement (p<0.05)."
        )
        
        # Assert
        assert "α" in abstract.reference_id
        assert "β-blockers" in abstract.title
        assert "p<0.05" in abstract.abstract_text
    
    def test_abstract_with_very_long_strings(self):
        """Test Abstract with very long strings."""
        # Arrange
        long_id = "A" * 100
        long_title = "B" * 1000
        long_abstract = "C" * 5000
        
        # Act
        abstract = Abstract(
            reference_id=long_id,
            title=long_title,
            abstract_text=long_abstract
        )
        
        # Assert
        assert len(abstract.reference_id) == 100
        assert len(abstract.title) == 1000
        assert len(abstract.abstract_text) == 5000
    
    def test_abstract_equality(self):
        """Test equality comparison between Abstract objects."""
        # Arrange
        abstract1 = Abstract(
            reference_id="REF001",
            title="Test Study",
            abstract_text="Test abstract",
            ground_truth="Include"
        )
        abstract2 = Abstract(
            reference_id="REF001",
            title="Test Study",
            abstract_text="Test abstract",
            ground_truth="Include"
        )
        abstract3 = Abstract(
            reference_id="REF002",
            title="Test Study",
            abstract_text="Test abstract",
            ground_truth="Include"
        )
        
        # Act & Assert
        assert abstract1 == abstract2
        assert abstract1 != abstract3


class TestAbstractEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_abstract_with_none_values_raises_error(self):
        """Test that None values raise appropriate errors."""
        # Test reference_id as None
        with pytest.raises(AttributeError):
            Abstract(
                reference_id=None,
                title="Test Study",
                abstract_text="Test abstract"
            )
    
    def test_abstract_with_numeric_strings(self):
        """Test Abstract with numeric strings."""
        # Arrange & Act
        abstract = Abstract(
            reference_id="12345",
            title="Study 456",
            abstract_text="This study included 789 participants."
        )
        
        # Assert
        assert abstract.reference_id == "12345"
        assert abstract.title == "Study 456"
        assert "789" in abstract.abstract_text
    
    def test_abstract_with_multiline_strings(self):
        """Test Abstract with multiline strings."""
        # Arrange & Act
        abstract = Abstract(
            reference_id="REF001",
            title="Multiline\nTitle",
            abstract_text="This is line 1.\nThis is line 2.\nThis is line 3."
        )
        
        # Assert
        assert "\n" in abstract.title
        assert "\n" in abstract.abstract_text
        assert "line 1" in abstract.abstract_text
        assert "line 3" in abstract.abstract_text
    
    def test_get_combined_text_with_multiline(self):
        """Test get_combined_text with multiline content."""
        # Arrange
        abstract = Abstract(
            reference_id="REF001",
            title="Line 1\nLine 2",
            abstract_text="Abstract line 1\nAbstract line 2"
        )
        
        # Act
        result = abstract.get_combined_text()
        
        # Assert
        expected = "Title: Line 1\nLine 2\n\nAbstract: Abstract line 1\nAbstract line 2"
        assert result == expected