"""
UCB Tutorial - Main Application
A professional interactive tutorial for understanding the Upper Confidence Bound algorithm
"""

import streamlit as st
from config import APP_CONFIG, STYLES
from ui_components import setup_page, render_sidebar
from tabs import (
    render_primer_tab,
    render_visual_tab,
    render_comparison_tab,
    render_statistical_tab,
    render_game_tab
)


def main():
    """Main application entry point"""
    # Page configuration
    setup_page()
    
    # Apply custom styling
    st.markdown(STYLES, unsafe_allow_html=True)
    
    # App header
    st.title("🎯 Upper Confidence Bound (UCB) Tutorial")
    st.markdown(
        """
        <div class='info-box'>
        An interactive tutorial to understand how the UCB algorithm balances 
        exploration and exploitation in multi-armed bandit problems.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render sidebar (only for non-game tabs)
    sidebar_config = render_sidebar()
    
    # Create tabs
    tabs = st.tabs([
        "📚 UCB Primer",
        "👁️ Visual Simulation",
        "📈 Compare Parameters",
        "🔬 Statistical Analysis",
        "🎮 Human vs UCB"
    ])
    
    # Render each tab
    with tabs[0]:
        render_primer_tab()
    
    with tabs[1]:
        render_visual_tab(sidebar_config)
    
    with tabs[2]:
        render_comparison_tab(sidebar_config)
    
    with tabs[3]:
        render_statistical_tab(sidebar_config)
    
    with tabs[4]:
        render_game_tab()  # Game tab doesn't use sidebar config


if __name__ == "__main__":
    main()
