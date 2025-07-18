"""
File Upload Component

This module provides the UI component for uploading CSV files.
Simplified for demo with validation and preview.
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List
import tempfile
import os

from ...data.processors import CSVProcessor
from ...data.models import Abstract


def show_file_upload() -> Optional[Dict[str, Any]]:
    """
    Show file upload interface.
    
    Returns:
        Optional[Dict]: File info and loaded abstracts, or None if no valid file
    """
    
    # Initialize CSV processor
    if 'csv_processor' not in st.session_state:
        st.session_state.csv_processor = CSVProcessor()
    
    csv_processor = st.session_state.csv_processor
    
    # File upload
    uploaded_file = st.file_uploader(
        "Choose CSV file",
        type=['csv'],
        help="Upload a CSV file containing abstracts with columns: Reference ID, Title, Abstract"
    )
    
    if uploaded_file is not None:
        try:
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_file_path = tmp_file.name
            
            try:
                # Validate file format
                validation_result = csv_processor.validate_csv_file(tmp_file_path)
                
                if validation_result['valid']:
                    # Load abstracts
                    abstracts = csv_processor.load_abstracts_from_csv(tmp_file_path)
                    
                    # Get file info
                    file_info = csv_processor.get_csv_info(tmp_file_path)
                    
                    # Show file summary
                    show_file_summary(file_info, abstracts)
                    
                    # Show sample abstracts
                    show_sample_abstracts(abstracts)
                    
                    # Clean up temp file
                    os.unlink(tmp_file_path)
                    
                    return {
                        'abstracts': abstracts,
                        'file_info': file_info,
                        'has_ground_truth': file_info.get('has_ground_truth', False),
                        'total_abstracts': len(abstracts)
                    }
                    
                else:
                    # Show validation errors
                    st.error("❌ File validation failed:")
                    
                    if 'missing_columns' in validation_result:
                        st.markdown("**Missing required columns:**")
                        for col in validation_result['missing_columns']:
                            st.markdown(f"- {col}")
                    
                    if 'error' in validation_result:
                        st.markdown(f"**Error:** {validation_result['error']}")
                    
                    # Show file format help
                    show_format_help()
                    
            finally:
                # Clean up temp file
                if os.path.exists(tmp_file_path):
                    os.unlink(tmp_file_path)
                    
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            show_format_help()
    
    else:
        # Show format requirements
        show_format_help()
    
    return None


def show_file_summary(file_info: Dict[str, Any], abstracts: List[Abstract]):
    """
    Show summary of uploaded file.
    
    Args:
        file_info: File information
        abstracts: Loaded abstracts
    """
    
    st.success("✅ File uploaded successfully!")
    
    # File statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total Abstracts", len(abstracts))
    
    with col2:
        st.metric("📊 Columns", len(file_info['columns']))
    
    with col3:
        has_ground_truth = file_info.get('has_ground_truth', False)
        st.metric("🎯 Ground Truth", "Yes" if has_ground_truth else "No")
    
    with col4:
        # Calculate average abstract length
        avg_length = sum(len(abs.abstract_text) for abs in abstracts) / len(abstracts)
        st.metric("📏 Avg Length", f"{avg_length:.0f} chars")
    
    # Show columns
    st.markdown("**📋 File Columns:**")
    cols_text = ", ".join(file_info['columns'])
    st.info(cols_text)
    
    # Show sample titles
    if file_info.get('sample_titles'):
        st.markdown("**📝 Sample Titles:**")
        for i, title in enumerate(file_info['sample_titles'][:3], 1):
            st.markdown(f"{i}. {title}")


def show_sample_abstracts(abstracts: List[Abstract]):
    """
    Show sample abstracts from the uploaded file.
    
    Args:
        abstracts: List of loaded abstracts
    """
    
    if not abstracts:
        return
    
    with st.expander("📖 Preview Sample Abstracts"):
        
        # Show first 3 abstracts
        for i, abstract in enumerate(abstracts[:3]):
            st.markdown(f"**Abstract {i+1}:**")
            
            col1, col2 = st.columns([1, 3])
            
            with col1:
                st.markdown(f"**ID:** {abstract.reference_id}")
                if abstract.ground_truth:
                    st.markdown(f"**Ground Truth:** {abstract.ground_truth}")
            
            with col2:
                st.markdown(f"**Title:** {abstract.title}")
                
                # Show truncated abstract
                abstract_preview = abstract.abstract_text[:200]
                if len(abstract.abstract_text) > 200:
                    abstract_preview += "..."
                st.markdown(f"**Abstract:** {abstract_preview}")
            
            st.markdown("---")


def show_format_help():
    """Show help information about expected file format."""
    
    st.markdown("### 📋 Expected File Format")
    
    st.info("""
    **Required CSV columns:**
    - **Reference ID**: Unique identifier for each abstract
    - **Title**: Title of the research paper
    - **Abstract**: Full abstract text
    
    **Optional columns:**
    - **Manual Decision**: Ground truth decisions (Include/Exclude) for accuracy comparison
    """)
    
    # Show sample CSV format
    with st.expander("📄 Sample CSV Format"):
        sample_data = {
            'Reference ID': ['REF001', 'REF002', 'REF003'],
            'Title': [
                'Effects of Metformin on Type 2 Diabetes',
                'ACE Inhibitors for Hypertension Treatment',
                'Cognitive Behavioral Therapy for Depression'
            ],
            'Abstract': [
                'This study examines the effects of metformin therapy on glycemic control in adults with type 2 diabetes...',
                'We investigated the efficacy of ACE inhibitors in reducing blood pressure in hypertensive patients...',
                'This randomized controlled trial evaluated the effectiveness of cognitive behavioral therapy...'
            ],
            'Manual Decision': ['Include', 'Exclude', 'Include']
        }
        
        sample_df = pd.DataFrame(sample_data)
        st.dataframe(sample_df, use_container_width=True)
        
        # Download sample CSV
        csv_data = sample_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Sample CSV",
            data=csv_data,
            file_name="sample_abstracts.csv",
            mime="text/csv"
        )


def show_upload_tips():
    """Show tips for successful file upload."""
    
    with st.expander("💡 Upload Tips"):
        st.markdown("""
        **For successful upload:**
        - Use UTF-8 encoding for special characters
        - Ensure no empty rows in critical columns
        - Keep file size under 200MB
        - Use standard CSV format (comma-separated)
        - Include column headers in the first row
        
        **Common Issues:**
        - Missing required columns
        - Empty Reference IDs or Abstract text
        - Inconsistent column names
        - File encoding problems
        """)


def validate_abstracts_quality(abstracts: List[Abstract]) -> Dict[str, Any]:
    """
    Validate the quality of loaded abstracts.
    
    Args:
        abstracts: List of abstracts to validate
        
    Returns:
        Dict: Validation results
    """
    
    if not abstracts:
        return {'valid': False, 'issues': ['No abstracts loaded']}
    
    issues = []
    warnings = []
    
    # Check for duplicates
    reference_ids = [abs.reference_id for abs in abstracts]
    if len(reference_ids) != len(set(reference_ids)):
        issues.append("Duplicate reference IDs found")
    
    # Check abstract lengths
    short_abstracts = [abs for abs in abstracts if len(abs.abstract_text) < 50]
    if short_abstracts:
        warnings.append(f"{len(short_abstracts)} abstracts are very short (< 50 characters)")
    
    # Check for missing titles
    missing_titles = [abs for abs in abstracts if not abs.title.strip()]
    if missing_titles:
        issues.append(f"{len(missing_titles)} abstracts have empty titles")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings,
        'total_abstracts': len(abstracts),
        'short_abstracts': len(short_abstracts)
    }