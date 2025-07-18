"""
Progress Display Component

This module provides the UI component for displaying processing progress.
Simplified for demo with real-time updates and statistics.
"""

import streamlit as st
import time
from typing import Dict, Any, Optional


def show_progress_display():
    """
    Show processing progress with real-time updates.
    
    Uses Streamlit session state to track and display progress.
    """
    
    # Get progress from session state
    progress = st.session_state.get('progress', 0)
    progress_text = st.session_state.get('progress_text', 'Initializing...')
    
    # Display progress bar
    st.markdown("### 🔄 Processing Progress")
    
    # Progress bar
    progress_bar = st.progress(progress)
    
    # Progress text
    status_text = st.empty()
    status_text.text(progress_text)
    
    # Processing statistics if available
    if 'processing_stats' in st.session_state:
        show_processing_stats(st.session_state.processing_stats)
    
    # Processing details
    show_processing_details()
    
    # Auto-refresh to update progress
    if st.session_state.get('processing', False):
        time.sleep(1)
        st.rerun()


def show_processing_stats(stats: Dict[str, Any]):
    """
    Show processing statistics.
    
    Args:
        stats: Processing statistics dictionary
    """
    
    st.markdown("#### 📊 Processing Statistics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Processed", stats.get('total_processed', 0))
    
    with col2:
        st.metric("✅ Successful", stats.get('successful', 0))
    
    with col3:
        st.metric("❌ Errors", stats.get('errors', 0))
    
    with col4:
        error_rate = stats.get('error_rate', 0)
        st.metric("📉 Error Rate", f"{error_rate:.1f}%")


def show_processing_details():
    """Show detailed processing information."""
    
    with st.expander("🔍 Processing Details"):
        
        # Current batch info
        if 'current_batch' in st.session_state:
            current_batch = st.session_state.current_batch
            total_batches = st.session_state.get('total_batches', 1)
            
            st.markdown(f"**Current Batch:** {current_batch} of {total_batches}")
            
            # Batch progress
            batch_progress = current_batch / total_batches if total_batches > 0 else 0
            st.progress(batch_progress)
        
        # Processing configuration
        batch_size = st.session_state.get('batch_size', 5)
        batch_delay = st.session_state.get('batch_delay', 1.0)
        
        st.markdown(f"**Batch Size:** {batch_size}")
        st.markdown(f"**Batch Delay:** {batch_delay}s")
        
        # Time estimates
        if 'start_time' in st.session_state:
            start_time = st.session_state.start_time
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            st.markdown(f"**Elapsed Time:** {elapsed_time:.1f}s")
            
            # Estimated remaining time
            progress = st.session_state.get('progress', 0)
            if progress > 0:
                estimated_total = elapsed_time / progress
                estimated_remaining = estimated_total - elapsed_time
                st.markdown(f"**Estimated Remaining:** {estimated_remaining:.1f}s")


def show_progress_with_callback(current: int, total: int, 
                               additional_info: Optional[Dict[str, Any]] = None):
    """
    Show progress with callback function for external use.
    
    Args:
        current: Current progress count
        total: Total items to process
        additional_info: Additional information to display
    """
    
    # Calculate progress percentage
    progress = current / total if total > 0 else 0
    
    # Update session state
    st.session_state.progress = progress
    st.session_state.progress_text = f"Processing: {current}/{total} ({progress*100:.1f}%)"
    
    # Update additional info if provided
    if additional_info:
        for key, value in additional_info.items():
            st.session_state[key] = value
    
    # Force UI update
    st.rerun()


def show_batch_progress(batch_info: Dict[str, Any]):
    """
    Show batch processing progress.
    
    Args:
        batch_info: Dictionary containing batch progress information
    """
    
    st.markdown("#### 📦 Batch Processing")
    
    current_batch = batch_info.get('current_batch', 0)
    total_batches = batch_info.get('total_batches', 1)
    
    # Batch progress bar
    batch_progress = current_batch / total_batches if total_batches > 0 else 0
    st.progress(batch_progress)
    
    # Batch details
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"**Current Batch:** {current_batch}")
        st.markdown(f"**Total Batches:** {total_batches}")
    
    with col2:
        completion_percentage = batch_info.get('completion_percentage', 0)
        st.markdown(f"**Completion:** {completion_percentage:.1f}%")
        
        processing_rate = batch_info.get('processing_rate', 0)
        st.markdown(f"**Rate:** {processing_rate:.1f} items/sec")
    
    # Time information
    if 'elapsed_time' in batch_info:
        elapsed_time = batch_info['elapsed_time']
        remaining_time = batch_info.get('estimated_remaining_time', 0)
        
        time_col1, time_col2 = st.columns(2)
        
        with time_col1:
            st.markdown(f"**Elapsed:** {elapsed_time:.1f}s")
        
        with time_col2:
            st.markdown(f"**Remaining:** {remaining_time:.1f}s")


def show_error_handling():
    """Show error handling information during processing."""
    
    if st.session_state.get('last_error'):
        st.error(f"⚠️ Last Error: {st.session_state.last_error}")
    
    # Error recovery options
    if st.session_state.get('processing_errors', 0) > 0:
        st.warning(f"⚠️ {st.session_state.processing_errors} errors encountered during processing")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Retry Failed Items"):
                st.session_state.retry_failed = True
                st.rerun()
        
        with col2:
            if st.button("⏭️ Skip and Continue"):
                st.session_state.skip_errors = True
                st.rerun()


def show_completion_summary():
    """Show completion summary when processing is done."""
    
    if not st.session_state.get('processing', False) and st.session_state.get('results'):
        st.success("🎉 Processing completed successfully!")
        
        # Show final statistics
        results = st.session_state.results
        total_processed = len(results)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📄 Total Processed", total_processed)
        
        with col2:
            included = sum(1 for r in results if r.is_included())
            st.metric("✅ Included", included)
        
        with col3:
            excluded = sum(1 for r in results if r.is_excluded())
            st.metric("❌ Excluded", excluded)
        
        # Processing time
        if 'start_time' in st.session_state:
            total_time = time.time() - st.session_state.start_time
            st.markdown(f"**Total Processing Time:** {total_time:.1f} seconds")
            
            if total_processed > 0:
                avg_time = total_time / total_processed
                st.markdown(f"**Average Time per Abstract:** {avg_time:.2f} seconds")


def init_progress_tracking():
    """Initialize progress tracking session state variables."""
    
    if 'progress' not in st.session_state:
        st.session_state.progress = 0
    
    if 'progress_text' not in st.session_state:
        st.session_state.progress_text = "Ready to start..."
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    if 'start_time' not in st.session_state:
        st.session_state.start_time = None
    
    if 'processing_stats' not in st.session_state:
        st.session_state.processing_stats = {}


def reset_progress_tracking():
    """Reset progress tracking to initial state."""
    
    st.session_state.progress = 0
    st.session_state.progress_text = "Ready to start..."
    st.session_state.processing = False
    st.session_state.start_time = None
    st.session_state.processing_stats = {}
    
    # Clear batch-specific state
    for key in ['current_batch', 'total_batches', 'last_error', 'processing_errors']:
        if key in st.session_state:
            del st.session_state[key]