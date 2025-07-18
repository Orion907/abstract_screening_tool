"""
Main Streamlit Application Entry Point

This is the main entry point for the Abstract Screening Tool demo.
Simplified for demo with essential UI components and workflow.
"""

import streamlit as st
import os
from pathlib import Path

# Set page config
st.set_page_config(
    page_title="Abstract Screening Tool - Demo",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Import UI components
from .ui.streamlit_app import main as streamlit_main

if __name__ == "__main__":
    streamlit_main()