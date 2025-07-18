"""
Main Streamlit UI Controller

This module contains the main Streamlit application interface.
Simplified for demo with essential components and workflow.
"""

import streamlit as st
import pandas as pd
import time
import os
from typing import Optional, List, Dict, Any

# Import core functionality
from ..core import ScreeningEngine, PICProcessor, BatchProcessor
from ..data.models import PICCriteria, Abstract, ScreeningResult
from ..data.processors import CSVProcessor

# Import UI components
from .components import criteria_input, file_upload, results_display, progress_display


def main():
    """Main Streamlit application function."""
    
    # Page header
    st.title("📋 Abstract Screening Tool - Demo")
    st.markdown("Automated systematic review screening using AI")
    
    # Initialize session state
    init_session_state()
    
    # Sidebar configuration
    setup_sidebar()
    
    # Main application flow
    if st.session_state.get('api_key_valid', False):
        show_main_application()
    else:
        show_api_key_setup()


def init_session_state():
    """Initialize Streamlit session state variables."""
    
    # API Configuration
    if 'api_key' not in st.session_state:
        st.session_state.api_key = ""
    if 'api_key_valid' not in st.session_state:
        st.session_state.api_key_valid = False
    if 'model_name' not in st.session_state:
        st.session_state.model_name = "gpt-3.5-turbo"
    
    # PIC Criteria
    if 'pic_criteria' not in st.session_state:
        st.session_state.pic_criteria = None
    if 'pic_text' not in st.session_state:
        st.session_state.pic_text = ""
    
    # File Upload
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    if 'abstracts' not in st.session_state:
        st.session_state.abstracts = []
    if 'file_info' not in st.session_state:
        st.session_state.file_info = {}
    
    # Processing
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'results' not in st.session_state:
        st.session_state.results = []
    if 'processing_stats' not in st.session_state:
        st.session_state.processing_stats = {}
    
    # Progress tracking
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    if 'progress_text' not in st.session_state:
        st.session_state.progress_text = ""


def setup_sidebar():
    """Setup sidebar with configuration options."""
    
    st.sidebar.header("⚙️ Configuration")
    
    # API Configuration
    with st.sidebar.expander("🔑 API Configuration", expanded=not st.session_state.get('api_key_valid', False)):
        
        # API Key input
        api_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.api_key,
            type="password",
            help="Enter your OpenAI API key"
        )
        
        # Model selection
        model_name = st.selectbox(
            "Model",
            ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
            index=0,
            help="Select the OpenAI model to use"
        )
        
        # Update session state
        st.session_state.api_key = api_key
        st.session_state.model_name = model_name
        
        # Validate API key
        if st.button("🔍 Validate API Key"):
            if validate_api_key(api_key, model_name):
                st.session_state.api_key_valid = True
                st.success("✅ API key validated successfully!")
                st.rerun()
            else:
                st.session_state.api_key_valid = False
                st.error("❌ Invalid API key or connection failed")
    
    # Processing Configuration
    if st.session_state.get('api_key_valid', False):
        with st.sidebar.expander("🔧 Processing Settings"):
            
            # Batch size
            batch_size = st.slider(
                "Batch Size",
                min_value=1,
                max_value=20,
                value=5,
                help="Number of abstracts to process in each batch"
            )
            
            # Delay between batches
            batch_delay = st.slider(
                "Batch Delay (seconds)",
                min_value=0.1,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Delay between batches to avoid API rate limits"
            )
            
            st.session_state.batch_size = batch_size
            st.session_state.batch_delay = batch_delay
    
    # Demo Information
    with st.sidebar.expander("ℹ️ Demo Information"):
        st.markdown("""
        **Features:**
        - PIC criteria-based screening
        - Batch processing with progress tracking
        - Ground truth comparison
        - Results export
        
        **Demo Limitations:**
        - OpenAI API required
        - Basic error handling
        - Simplified UI
        """)


def show_api_key_setup():
    """Show API key setup interface."""
    
    st.info("🔑 Please configure your OpenAI API key in the sidebar to begin.")
    
    # Demo instructions
    st.markdown("""
    ### Getting Started
    
    1. **Get an OpenAI API key** from [OpenAI Platform](https://platform.openai.com/api-keys)
    2. **Enter your API key** in the sidebar
    3. **Click 'Validate API Key'** to verify connection
    4. **Begin screening** your abstracts!
    
    ### What This Demo Does
    
    This tool automates the screening of research abstracts for systematic reviews using:
    - **PIC criteria** (Population, Intervention, Comparator)
    - **AI-powered screening** with OpenAI's GPT models
    - **Batch processing** for efficiency
    - **Progress tracking** and statistics
    - **Ground truth comparison** for accuracy assessment
    """)


def show_main_application():
    """Show the main application interface."""
    
    # Create main tabs
    tab1, tab2, tab3 = st.tabs(["📝 Setup", "🔄 Processing", "📊 Results"])
    
    with tab1:
        show_setup_tab()
    
    with tab2:
        show_processing_tab()
    
    with tab3:
        show_results_tab()


def show_setup_tab():
    """Show the setup tab with PIC criteria and file upload."""
    
    st.header("📝 Setup Screening Criteria and Data")
    
    # PIC Criteria Input
    st.subheader("1. 📋 PIC Criteria")
    pic_criteria = criteria_input.show_criteria_input()
    
    if pic_criteria:
        st.session_state.pic_criteria = pic_criteria
        st.success("✅ PIC criteria configured")
    
    # File Upload
    st.subheader("2. 📁 Upload Abstract Data")
    file_info = file_upload.show_file_upload()
    
    if file_info and file_info.get('abstracts'):
        st.session_state.abstracts = file_info['abstracts']
        st.session_state.file_info = file_info
        st.success(f"✅ {len(file_info['abstracts'])} abstracts loaded")
    
    # Ready to process check
    if st.session_state.pic_criteria and st.session_state.abstracts:
        st.success("🎉 Ready to begin screening! Go to the Processing tab.")


def show_processing_tab():
    """Show the processing tab with batch processing controls."""
    
    st.header("🔄 Abstract Screening Processing")
    
    # Check if setup is complete
    if not st.session_state.pic_criteria:
        st.warning("⚠️ Please configure PIC criteria in the Setup tab first.")
        return
    
    if not st.session_state.abstracts:
        st.warning("⚠️ Please upload abstract data in the Setup tab first.")
        return
    
    # Display current configuration
    col1, col2 = st.columns(2)
    
    with col1:
        st.info(f"📊 **{len(st.session_state.abstracts)} abstracts** ready for screening")
        
        # Show PIC criteria summary
        st.markdown("**PIC Criteria:**")
        st.markdown(f"- **Population:** {st.session_state.pic_criteria.population[:50]}...")
        st.markdown(f"- **Intervention:** {st.session_state.pic_criteria.intervention[:50]}...")
        st.markdown(f"- **Comparator:** {st.session_state.pic_criteria.comparator[:50]}...")
    
    with col2:
        # Processing estimates
        batch_processor = BatchProcessor(
            batch_size=st.session_state.get('batch_size', 5),
            delay_between_batches=st.session_state.get('batch_delay', 1.0)
        )
        
        estimates = batch_processor.estimate_processing_time(len(st.session_state.abstracts))
        
        st.info(f"⏱️ **Estimated processing time:** {estimates['estimated_total_time_minutes']:.1f} minutes")
        st.markdown(f"- **Batches:** {estimates['total_batches']}")
        st.markdown(f"- **Batch size:** {estimates['batch_size']}")
    
    # Start processing button
    if not st.session_state.processing:
        if st.button("🚀 Start Screening", type="primary", use_container_width=True):
            start_processing()
    else:
        st.info("🔄 Processing in progress...")
        if st.button("🛑 Stop Processing", type="secondary"):
            st.session_state.processing = False
            st.rerun()
    
    # Show progress if processing
    if st.session_state.processing:
        progress_display.show_progress_display()


def show_results_tab():
    """Show the results tab with screening results and statistics."""
    
    st.header("📊 Screening Results")
    
    if not st.session_state.results:
        st.info("ℹ️ No screening results yet. Complete processing to see results here.")
        return
    
    # Display results
    results_display.show_results_display(
        st.session_state.results,
        st.session_state.abstracts,
        st.session_state.file_info.get('has_ground_truth', False)
    )


def validate_api_key(api_key: str, model_name: str) -> bool:
    """
    Validate the OpenAI API key.
    
    Args:
        api_key: The API key to validate
        model_name: The model name to test
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not api_key:
        return False
    
    try:
        # Create screening engine to test connection
        engine = ScreeningEngine(api_key, model_name)
        validation_result = engine.validate_setup()
        return validation_result['valid']
    except Exception:
        return False


def start_processing():
    """Start the abstract screening process."""
    
    st.session_state.processing = True
    st.session_state.progress = 0
    st.session_state.progress_text = "Initializing..."
    
    # Initialize components
    screening_engine = ScreeningEngine(
        st.session_state.api_key,
        st.session_state.model_name
    )
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def update_progress(current: int, total: int):
        """Update progress display."""
        progress = current / total
        st.session_state.progress = progress
        progress_bar.progress(progress)
        status_text.text(f"Processing: {current}/{total} abstracts ({progress*100:.1f}%)")
    
    try:
        # Process abstracts
        status_text.text("🔄 Starting screening process...")
        
        results = screening_engine.process_screening_batch(
            st.session_state.pic_criteria,
            st.session_state.abstracts,
            progress_callback=update_progress
        )
        
        # Store results
        st.session_state.results = results
        st.session_state.processing_stats = screening_engine.get_screening_stats(results)
        
        # Show completion
        status_text.text("✅ Screening completed successfully!")
        st.success(f"🎉 Completed screening {len(results)} abstracts!")
        
        # Auto-switch to results tab
        time.sleep(2)
        st.session_state.processing = False
        st.rerun()
        
    except Exception as e:
        st.error(f"❌ Processing failed: {str(e)}")
        st.session_state.processing = False
        st.rerun()


if __name__ == "__main__":
    main()