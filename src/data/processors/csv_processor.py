"""
CSV Processor

This module handles CSV file processing for the demo implementation.
Hard-coded for the known demo CSV format to simplify processing.
"""

import pandas as pd
from typing import List, Dict, Optional
from pathlib import Path

from ..models import Abstract


class CSVProcessor:
    """
    Processes CSV files containing research abstracts.
    
    Demo version assumes specific column structure and provides basic error handling.
    """
    
    # Hard-coded column mappings for demo CSV format
    EXPECTED_COLUMNS = {
        'Reference ID': 'reference_id',
        'Title': 'title', 
        'Abstract': 'abstract_text',
        'Manual Decision': 'ground_truth'  # For comparison with expert decisions
    }
    
    def __init__(self):
        """Initialize CSV processor with demo configuration."""
        pass
    
    def load_abstracts_from_csv(self, file_path: str) -> List[Abstract]:
        """
        Load abstracts from CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            List[Abstract]: List of loaded abstracts
            
        Raises:
            ValueError: If file format is invalid
            FileNotFoundError: If file doesn't exist
        """
        try:
            # Load CSV file
            df = pd.read_csv(file_path)
            
            # Validate expected columns exist
            self._validate_csv_columns(df)
            
            # Convert to Abstract objects
            abstracts = []
            for _, row in df.iterrows():
                try:
                    abstract = Abstract(
                        reference_id=str(row['Reference ID']),
                        title=str(row['Title']),
                        abstract_text=str(row['Abstract']),
                        ground_truth=str(row['Manual Decision']) if pd.notna(row.get('Manual Decision')) else None
                    )
                    abstracts.append(abstract)
                except Exception as e:
                    # Skip invalid rows but log the issue
                    print(f"Warning: Skipping row with Reference ID {row.get('Reference ID', 'Unknown')}: {e}")
                    continue
            
            return abstracts
            
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {file_path}")
        except Exception as e:
            raise ValueError(f"Error processing CSV file: {e}")
    
    def _validate_csv_columns(self, df: pd.DataFrame) -> None:
        """
        Validate that CSV has expected columns.
        
        Args:
            df: DataFrame to validate
            
        Raises:
            ValueError: If required columns are missing
        """
        required_columns = ['Reference ID', 'Title', 'Abstract']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
    
    def save_results_to_csv(self, abstracts: List[Abstract], results: List[Dict], 
                           output_path: str) -> None:
        """
        Save screening results to CSV file.
        
        Args:
            abstracts: List of original abstracts
            results: List of screening results
            output_path: Path for output CSV file
        """
        try:
            # Create results DataFrame
            results_data = []
            
            # Create lookup for results by reference_id
            results_lookup = {result['reference_id']: result for result in results}
            
            for abstract in abstracts:
                result = results_lookup.get(abstract.reference_id, {})
                
                row = {
                    'Reference ID': abstract.reference_id,
                    'Title': abstract.title,
                    'Abstract': abstract.abstract_text,
                    'AI Decision': result.get('decision', 'Not Processed'),
                    'AI Reasoning': result.get('reasoning', 'Not Processed'),
                    'Manual Decision': abstract.ground_truth or 'Not Available'
                }
                results_data.append(row)
            
            # Save to CSV
            df = pd.DataFrame(results_data)
            df.to_csv(output_path, index=False)
            
        except Exception as e:
            raise ValueError(f"Error saving results to CSV: {e}")
    
    def get_csv_info(self, file_path: str) -> Dict:
        """
        Get basic information about a CSV file.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dict: Information about the CSV file
        """
        try:
            df = pd.read_csv(file_path)
            
            return {
                'total_rows': len(df),
                'columns': list(df.columns),
                'has_ground_truth': 'Manual Decision' in df.columns,
                'sample_titles': df['Title'].head(3).tolist() if 'Title' in df.columns else []
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def validate_csv_file(self, file_path: str) -> Dict:
        """
        Validate CSV file format and content.
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Dict: Validation results
        """
        try:
            df = pd.read_csv(file_path)
            
            # Check required columns
            required_columns = ['Reference ID', 'Title', 'Abstract']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            # Check for empty rows
            empty_rows = df.isnull().all(axis=1).sum()
            
            # Check for missing critical data
            missing_ids = df['Reference ID'].isnull().sum() if 'Reference ID' in df.columns else 0
            missing_abstracts = df['Abstract'].isnull().sum() if 'Abstract' in df.columns else 0
            
            return {
                'valid': len(missing_columns) == 0,
                'missing_columns': missing_columns,
                'total_rows': len(df),
                'empty_rows': empty_rows,
                'missing_reference_ids': missing_ids,
                'missing_abstracts': missing_abstracts,
                'warnings': []
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': str(e)
            }