"""
PIC Criteria Input Component

This module provides the UI component for inputting PIC criteria.
Simplified for demo with template options and validation.
"""

import streamlit as st
from typing import Optional

from ...core import PICProcessor
from ...data.models import PICCriteria


def show_criteria_input() -> Optional[PICCriteria]:
    """
    Show PIC criteria input interface.
    
    Returns:
        Optional[PICCriteria]: Parsed PIC criteria or None if invalid
    """
    
    # Initialize PIC processor
    if 'pic_processor' not in st.session_state:
        st.session_state.pic_processor = PICProcessor()
    
    pic_processor = st.session_state.pic_processor
    
    # Template selection
    st.markdown("**Choose a template or enter custom criteria:**")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        template_option = st.selectbox(
            "Template",
            [
                "Custom (enter below)",
                "Type 2 Diabetes - Metformin",
                "Hypertension - ACE Inhibitors", 
                "Depression - CBT",
                "Cancer - Chemotherapy",
                "Chronic Pain - Analgesics"
            ],
            help="Select a pre-defined template or choose Custom to enter your own criteria"
        )
    
    with col2:
        if st.button("📋 Use Template"):
            if template_option != "Custom (enter below)":
                template_text = get_template_text(template_option)
                st.session_state.pic_text = template_text
                st.rerun()
    
    # Text input area
    pic_text = st.text_area(
        "PIC Criteria",
        value=st.session_state.get('pic_text', pic_processor.create_pic_template()),
        height=200,
        help="Enter your PIC criteria. Use format: Population: ..., Intervention: ..., Comparator: ..."
    )
    
    # Update session state
    st.session_state.pic_text = pic_text
    
    # Parse and validate
    if pic_text and pic_text.strip():
        try:
            # Parse PIC criteria
            pic_criteria = pic_processor.parse_pic_from_text(pic_text)
            
            # Validate completeness
            validation = pic_processor.validate_pic_completeness(pic_criteria)
            
            # Show validation results
            if validation['valid']:
                st.success("✅ PIC criteria parsed successfully!")
                
                # Show parsed criteria
                with st.expander("📋 Parsed PIC Criteria"):
                    st.markdown(f"**Population:** {pic_criteria.population}")
                    st.markdown(f"**Intervention:** {pic_criteria.intervention}")
                    st.markdown(f"**Comparator:** {pic_criteria.comparator}")
                
                # Show warnings if any
                if validation['warnings']:
                    st.warning("⚠️ Validation warnings:")
                    for warning in validation['warnings']:
                        st.markdown(f"- {warning}")
                
                return pic_criteria
            else:
                st.error("❌ PIC criteria validation failed")
                for issue in validation['issues']:
                    st.markdown(f"- {issue}")
                
        except ValueError as e:
            st.error(f"❌ Error parsing PIC criteria: {str(e)}")
            
            # Show suggestions
            suggestions = pic_processor.get_pic_suggestions(pic_text)
            if suggestions:
                st.info("💡 Suggestions:")
                for suggestion in suggestions:
                    if st.button(f"Use: {suggestion[:50]}...", key=f"suggestion_{hash(suggestion)}"):
                        st.session_state.pic_text = suggestion
                        st.rerun()
    
    return None


def get_template_text(template_option: str) -> str:
    """
    Get template text for selected option.
    
    Args:
        template_option: Selected template option
        
    Returns:
        str: Template text
    """
    
    templates = {
        "Type 2 Diabetes - Metformin": """Population: Adults with Type 2 diabetes mellitus

Intervention: Metformin therapy (any dose or formulation)

Comparator: Placebo or standard care without metformin""",
        
        "Hypertension - ACE Inhibitors": """Population: Adults with hypertension (blood pressure ≥140/90 mmHg)

Intervention: ACE inhibitor therapy (any ACE inhibitor)

Comparator: Placebo or other antihypertensive medications""",
        
        "Depression - CBT": """Population: Adults with major depressive disorder

Intervention: Cognitive behavioral therapy (CBT)

Comparator: Standard care, waitlist control, or other psychotherapy""",
        
        "Cancer - Chemotherapy": """Population: Adults with cancer (any type)

Intervention: Chemotherapy treatment (any regimen)

Comparator: Standard care, placebo, or alternative treatments""",
        
        "Chronic Pain - Analgesics": """Population: Adults with chronic pain (duration ≥3 months)

Intervention: Analgesic medication (any type)

Comparator: Placebo or alternative pain management strategies"""
    }
    
    return templates.get(template_option, "")


def show_criteria_preview(pic_criteria: PICCriteria):
    """
    Show a preview of the PIC criteria.
    
    Args:
        pic_criteria: PIC criteria to preview
    """
    
    st.markdown("### 📋 PIC Criteria Preview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**👥 Population**")
        st.info(pic_criteria.population)
    
    with col2:
        st.markdown("**💊 Intervention**")
        st.info(pic_criteria.intervention)
    
    with col3:
        st.markdown("**🔄 Comparator**")
        st.info(pic_criteria.comparator)