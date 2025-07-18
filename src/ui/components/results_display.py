"""
Results Display Component

This module provides the UI component for displaying screening results.
Simplified for demo with statistics, comparison, and export functionality.
"""

import streamlit as st
import pandas as pd
from typing import List, Dict, Any, Optional
import io

from ...data.models import Abstract, ScreeningResult, ScreeningDecision
from ...core import ScreeningEngine


def show_results_display(results: List[ScreeningResult], 
                        abstracts: List[Abstract], 
                        has_ground_truth: bool = False):
    """
    Show screening results with statistics and export options.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
        has_ground_truth: Whether ground truth data is available
    """
    
    if not results:
        st.info("ℹ️ No results to display")
        return
    
    # Display summary statistics
    show_results_summary(results, abstracts, has_ground_truth)
    
    # Show ground truth comparison if available
    if has_ground_truth:
        show_ground_truth_comparison(results, abstracts)
    
    # Display detailed results
    show_detailed_results(results, abstracts)
    
    # Export options
    show_export_options(results, abstracts)


def show_results_summary(results: List[ScreeningResult], 
                        abstracts: List[Abstract], 
                        has_ground_truth: bool):
    """
    Display summary statistics for screening results.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
        has_ground_truth: Whether ground truth data is available
    """
    
    st.subheader("📊 Screening Summary")
    
    # Calculate statistics
    total_processed = len(results)
    included = sum(1 for r in results if r.is_included())
    excluded = sum(1 for r in results if r.is_excluded())
    errors = sum(1 for r in results if r.decision == ScreeningDecision.ERROR)
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📄 Total Processed", total_processed)
    
    with col2:
        st.metric("✅ Included", included, f"{(included/total_processed)*100:.1f}%")
    
    with col3:
        st.metric("❌ Excluded", excluded, f"{(excluded/total_processed)*100:.1f}%")
    
    with col4:
        st.metric("⚠️ Errors", errors, f"{(errors/total_processed)*100:.1f}%")


def show_ground_truth_comparison(results: List[ScreeningResult], 
                                abstracts: List[Abstract]):
    """
    Show comparison with ground truth data.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
    """
    
    st.subheader("🎯 Ground Truth Comparison")
    
    # Create ground truth lookup
    ground_truth_lookup = {
        abstract.reference_id: abstract.ground_truth 
        for abstract in abstracts 
        if abstract.ground_truth
    }
    
    if not ground_truth_lookup:
        st.info("ℹ️ No ground truth data available for comparison")
        return
    
    # Calculate comparison metrics
    total_compared = 0
    agreements = 0
    disagreements = []
    
    for result in results:
        if result.reference_id in ground_truth_lookup:
            ground_truth = ground_truth_lookup[result.reference_id]
            ai_decision = result.decision.value
            
            if ground_truth.lower() == ai_decision.lower():
                agreements += 1
            else:
                disagreements.append({
                    'Reference ID': result.reference_id,
                    'Ground Truth': ground_truth,
                    'AI Decision': ai_decision,
                    'AI Reasoning': result.reasoning[:100] + "..." if len(result.reasoning) > 100 else result.reasoning
                })
            
            total_compared += 1
    
    # Display comparison metrics
    if total_compared > 0:
        accuracy = (agreements / total_compared) * 100
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔍 Compared", total_compared)
        
        with col2:
            st.metric("✅ Agreements", agreements, f"{accuracy:.1f}%")
        
        with col3:
            st.metric("❌ Disagreements", len(disagreements), f"{100-accuracy:.1f}%")
        
        # Show disagreements if any
        if disagreements:
            with st.expander(f"📋 View {len(disagreements)} Disagreements"):
                disagreements_df = pd.DataFrame(disagreements)
                st.dataframe(disagreements_df, use_container_width=True)


def show_detailed_results(results: List[ScreeningResult], 
                         abstracts: List[Abstract]):
    """
    Show detailed results table with filtering options.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
    """
    
    st.subheader("📋 Detailed Results")
    
    # Create abstracts lookup
    abstracts_lookup = {abs.reference_id: abs for abs in abstracts}
    
    # Filter options
    col1, col2 = st.columns(2)
    
    with col1:
        decision_filter = st.selectbox(
            "Filter by Decision",
            ["All", "Include", "Exclude", "Error"],
            help="Filter results by screening decision"
        )
    
    with col2:
        search_text = st.text_input(
            "Search Results",
            placeholder="Search by Reference ID or reasoning...",
            help="Search in reference IDs or reasoning text"
        )
    
    # Apply filters
    filtered_results = results
    
    if decision_filter != "All":
        filtered_results = [r for r in filtered_results if r.decision.value == decision_filter]
    
    if search_text:
        search_lower = search_text.lower()
        filtered_results = [
            r for r in filtered_results 
            if search_lower in r.reference_id.lower() or search_lower in r.reasoning.lower()
        ]
    
    # Create results dataframe
    results_data = []
    for result in filtered_results:
        abstract = abstracts_lookup.get(result.reference_id)
        
        row = {
            'Reference ID': result.reference_id,
            'Title': abstract.title[:100] + "..." if abstract and len(abstract.title) > 100 else (abstract.title if abstract else ""),
            'Decision': result.decision.value,
            'Reasoning': result.reasoning[:200] + "..." if len(result.reasoning) > 200 else result.reasoning,
            'Ground Truth': abstract.ground_truth if abstract else None
        }
        results_data.append(row)
    
    if results_data:
        results_df = pd.DataFrame(results_data)
        
        # Show results count
        st.info(f"📊 Showing {len(results_data)} of {len(results)} results")
        
        # Display results table
        st.dataframe(
            results_df, 
            use_container_width=True,
            height=400
        )
        
        # Expandable detailed view
        with st.expander("🔍 View Full Details"):
            selected_id = st.selectbox(
                "Select Reference ID for full details",
                [r['Reference ID'] for r in results_data],
                key="detailed_view_select"
            )
            
            if selected_id:
                selected_result = next(r for r in results if r.reference_id == selected_id)
                selected_abstract = abstracts_lookup.get(selected_id)
                
                show_single_result_details(selected_result, selected_abstract)
    
    else:
        st.info("ℹ️ No results match the current filters")


def show_single_result_details(result: ScreeningResult, abstract: Optional[Abstract]):
    """
    Show detailed view of a single screening result.
    
    Args:
        result: Screening result to display
        abstract: Original abstract (if available)
    """
    
    st.markdown(f"### 📄 {result.reference_id}")
    
    if abstract:
        st.markdown(f"**Title:** {abstract.title}")
        st.markdown(f"**Abstract:** {abstract.abstract_text}")
        
        if abstract.ground_truth:
            st.markdown(f"**Ground Truth:** {abstract.ground_truth}")
    
    # Screening result
    decision_color = {
        "Include": "🟢",
        "Exclude": "🔴", 
        "Error": "🟡"
    }
    
    st.markdown(f"**AI Decision:** {decision_color.get(result.decision.value, '')} {result.decision.value}")
    st.markdown(f"**AI Reasoning:** {result.reasoning}")
    
    if result.confidence:
        st.markdown(f"**Confidence:** {result.confidence:.2f}")


def show_export_options(results: List[ScreeningResult], 
                       abstracts: List[Abstract]):
    """
    Show export options for screening results.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
    """
    
    st.subheader("📥 Export Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Export as CSV
        csv_data = create_results_csv(results, abstracts)
        st.download_button(
            label="📄 Download CSV",
            data=csv_data,
            file_name="screening_results.csv",
            mime="text/csv",
            help="Download results as CSV file"
        )
    
    with col2:
        # Export summary report
        summary_data = create_summary_report(results, abstracts)
        st.download_button(
            label="📊 Download Summary Report",
            data=summary_data,
            file_name="screening_summary.txt",
            mime="text/plain",
            help="Download summary report as text file"
        )


def create_results_csv(results: List[ScreeningResult], 
                      abstracts: List[Abstract]) -> str:
    """
    Create CSV data for results export.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
        
    Returns:
        str: CSV data as string
    """
    
    # Create abstracts lookup
    abstracts_lookup = {abs.reference_id: abs for abs in abstracts}
    
    # Create results data
    results_data = []
    for result in results:
        abstract = abstracts_lookup.get(result.reference_id)
        
        row = {
            'Reference ID': result.reference_id,
            'Title': abstract.title if abstract else "",
            'Abstract': abstract.abstract_text if abstract else "",
            'AI Decision': result.decision.value,
            'AI Reasoning': result.reasoning,
            'Ground Truth': abstract.ground_truth if abstract else "",
            'Confidence': result.confidence if result.confidence else ""
        }
        results_data.append(row)
    
    # Convert to CSV
    df = pd.DataFrame(results_data)
    return df.to_csv(index=False)


def create_summary_report(results: List[ScreeningResult], 
                         abstracts: List[Abstract]) -> str:
    """
    Create summary report for export.
    
    Args:
        results: List of screening results
        abstracts: List of original abstracts
        
    Returns:
        str: Summary report as text
    """
    
    # Calculate statistics
    total_processed = len(results)
    included = sum(1 for r in results if r.is_included())
    excluded = sum(1 for r in results if r.is_excluded())
    errors = sum(1 for r in results if r.decision == ScreeningDecision.ERROR)
    
    # Create ground truth comparison if available
    ground_truth_lookup = {
        abstract.reference_id: abstract.ground_truth 
        for abstract in abstracts 
        if abstract.ground_truth
    }
    
    accuracy_text = ""
    if ground_truth_lookup:
        total_compared = 0
        agreements = 0
        
        for result in results:
            if result.reference_id in ground_truth_lookup:
                ground_truth = ground_truth_lookup[result.reference_id]
                ai_decision = result.decision.value
                
                if ground_truth.lower() == ai_decision.lower():
                    agreements += 1
                
                total_compared += 1
        
        if total_compared > 0:
            accuracy = (agreements / total_compared) * 100
            accuracy_text = f"""
Ground Truth Comparison:
- Total Compared: {total_compared}
- Agreements: {agreements}
- Accuracy: {accuracy:.1f}%
"""
    
    # Create report
    report = f"""Abstract Screening Results Summary
=====================================

Processing Statistics:
- Total Processed: {total_processed}
- Included: {included} ({(included/total_processed)*100:.1f}%)
- Excluded: {excluded} ({(excluded/total_processed)*100:.1f}%)
- Errors: {errors} ({(errors/total_processed)*100:.1f}%)

{accuracy_text}

Generated by Abstract Screening Tool - Demo
"""
    
    return report