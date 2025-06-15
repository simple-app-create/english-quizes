#!/usr/bin/env python3
"""
Theme Management for English Quiz App

Handles light/dark theme switching and CSS injection for Streamlit.
"""

import streamlit as st


class ThemeManager:
    """Manage themes for the quiz application"""
    
    # Available themes
    THEMES = {
        'light': 'Light Theme',
        'dark': 'Dark Theme'
    }
    
    # Default theme
    DEFAULT_THEME = 'light'
    
    @staticmethod
    def initialize_theme_state():
        """Initialize theme in session state if not present"""
        if 'theme' not in st.session_state:
            st.session_state.theme = ThemeManager.DEFAULT_THEME
    
    @staticmethod
    def get_current_theme():
        """Get the current theme from session state"""
        return st.session_state.get('theme', ThemeManager.DEFAULT_THEME)
    
    @staticmethod
    def set_theme(theme_name):
        """Set the current theme and apply it"""
        if theme_name in ThemeManager.THEMES:
            st.session_state.theme = theme_name
            ThemeManager.apply_current_theme()
    
    @staticmethod
    def get_available_themes():
        """Get list of available themes"""
        return ThemeManager.THEMES
    
    @staticmethod
    def apply_current_theme():
        """Apply the current theme's CSS"""
        theme = ThemeManager.get_current_theme()
        
        if theme == 'dark':
            ThemeManager._apply_dark_theme()
        else:
            ThemeManager._apply_light_theme()
    
    @staticmethod
    def _apply_dark_theme():
        """Apply dark theme CSS"""
        st.markdown("""
        <style>
            /* Dark Theme Styles */
            
            /* Main background */
            .stApp {
                background-color: #0e1117;
                color: #fafafa;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background-color: #262730;
            }
            
            /* Text inputs and selectboxes */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div {
                background-color: #262730;
                color: #fafafa;
                border-color: #4a4a4a;
            }
            
            /* Buttons */
            .stButton > button {
                background-color: #262730;
                color: #fafafa;
                border-color: #4a4a4a;
                transition: all 0.2s ease;
            }
            
            .stButton > button:hover {
                background-color: #3a3a3a;
                border-color: #6a6a6a;
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            
            /* Primary buttons */
            .stButton > button[kind="primary"] {
                background-color: #1f77b4;
                border-color: #1f77b4;
            }
            
            .stButton > button[kind="primary"]:hover {
                background-color: #0d5a8b;
                border-color: #0d5a8b;
            }
            
            /* Secondary buttons */
            .stButton > button[kind="secondary"] {
                background-color: #4a4a4a;
                border-color: #6a6a6a;
                color: #fafafa;
            }
            
            .stButton > button[kind="secondary"]:hover {
                background-color: #5a5a5a;
                border-color: #7a7a7a;
            }
            
            /* Cards and containers */
            .element-container {
                background-color: #262730;
            }
            
            /* Success/Error messages */
            .stSuccess {
                background-color: #1e3a1e;
                border-color: #2e5c2e;
                color: #90ee90;
            }
            
            .stError {
                background-color: #3a1e1e;
                border-color: #5c2e2e;
                color: #ffcccb;
            }
            
            .stInfo {
                background-color: #1e2a3a;
                border-color: #2e4c5c;
                color: #add8e6;
            }
            
            /* Radio buttons */
            .stRadio > div {
                background-color: #262730;
                padding: 0.5rem;
                border-radius: 0.3rem;
            }
            
            .stRadio > div label {
                color: #fafafa;
            }
            
            /* Progress bars */
            .stProgress > div > div {
                background-color: #1f77b4;
            }
            
            /* Markdown content */
            .stMarkdown {
                color: #fafafa;
            }
            
            /* Headers */
            h1, h2, h3, h4, h5, h6 {
                color: #fafafa !important;
            }
            
            /* Quiz question styling */
            .quiz-question {
                background-color: #262730;
                padding: 1.5rem;
                border-radius: 0.5rem;
                border: 1px solid #4a4a4a;
                margin: 1rem 0;
                box-shadow: 0 4px 8px rgba(0,0,0,0.3);
            }
            
            .quiz-question h3, .quiz-question h4 {
                color: #fafafa !important;
                margin-top: 0;
            }
            
            .quiz-question p {
                color: #d0d0d0;
            }
            
            .quiz-question blockquote {
                background-color: #1a1a1a;
                border-left: 4px solid #1f77b4;
                padding: 1rem;
                margin: 1rem 0;
                color: #e0e0e0;
            }
            
            /* Metrics */
            .metric-container {
                background-color: #262730;
                padding: 1rem;
                border-radius: 0.3rem;
            }
            
            /* Selectbox dropdown */
            .stSelectbox > div > div > div > div {
                background-color: #262730;
                color: #fafafa;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def _apply_light_theme():
        """Apply light theme CSS"""
        st.markdown("""
        <style>
            /* Light Theme Styles */
            
            /* Main background and text */
            .stApp {
                background-color: #ffffff;
                color: #262730;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background-color: #f0f2f6;
                color: #262730;
            }
            
            /* All text elements - force dark colors */
            body, p, div, span, li, td, th {
                color: #262730 !important;
            }
            
            /* Headers - ensure they're dark */
            h1, h2, h3, h4, h5, h6 {
                color: #1f2937 !important;
            }
            
            /* Streamlit specific text elements */
            .stMarkdown, .stMarkdown p, .stMarkdown div {
                color: #262730 !important;
            }
            
            /* Sidebar text */
            .css-1d391kg p, .css-1d391kg div, .css-1d391kg span {
                color: #262730 !important;
            }
            
            /* Text inputs and selectboxes */
            .stTextInput > div > div > input,
            .stSelectbox > div > div > div {
                background-color: #ffffff;
                color: #262730 !important;
                border-color: #d1d5db;
            }
            
            /* Selectbox dropdown */
            .stSelectbox > div > div > div > div {
                background-color: #ffffff;
                color: #262730 !important;
            }
            
            /* Enhanced buttons */
            .stButton > button {
                transition: all 0.2s ease;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                border: 1px solid #d1d5db;
                background-color: #ffffff;
                color: #262730 !important;
            }
            
            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.15);
                border-color: #9ca3af;
                background-color: #f9fafb;
            }
            
            /* Primary buttons */
            .stButton > button[kind="primary"] {
                background-color: #1f77b4;
                border-color: #1f77b4;
                color: white !important;
            }
            
            .stButton > button[kind="primary"]:hover {
                background-color: #0d5a8b;
                border-color: #0d5a8b;
                color: white !important;
            }
            
            /* Secondary buttons */
            .stButton > button[kind="secondary"] {
                background-color: #f8f9fa;
                border-color: #d1d5db;
                color: #374151 !important;
            }
            
            .stButton > button[kind="secondary"]:hover {
                background-color: #e5e7eb;
                border-color: #9ca3af;
                color: #374151 !important;
            }
            
            /* Quiz question styling */
            .quiz-question {
                background-color: #f8f9fa;
                padding: 1.5rem;
                border-radius: 0.5rem;
                border: 1px solid #e1e5e9;
                margin: 1rem 0;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .quiz-question h3, .quiz-question h4 {
                color: #1f2937 !important;
                margin-top: 0;
            }
            
            .quiz-question p {
                color: #4b5563 !important;
            }
            
            .quiz-question blockquote {
                background-color: #f3f4f6;
                border-left: 4px solid #1f77b4;
                padding: 1rem;
                margin: 1rem 0;
                color: #374151 !important;
            }
            
            /* Radio buttons enhancement */
            .stRadio > div {
                background-color: #ffffff;
                padding: 0.5rem;
                border-radius: 0.3rem;
                border: 1px solid #e5e7eb;
            }
            
            .stRadio > div:hover {
                border-color: #d1d5db;
                box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            }
            
            .stRadio > div label {
                color: #262730 !important;
            }
            
            .stRadio > div label span {
                color: #262730 !important;
            }
            
            /* Progress bar */
            .stProgress > div > div {
                background-color: #1f77b4;
            }
            
            /* Success/Error/Info messages */
            .stSuccess {
                border-left: 4px solid #10b981;
                background-color: #f0fdf4;
                color: #166534 !important;
            }
            
            .stError {
                border-left: 4px solid #ef4444;
                background-color: #fef2f2;
                color: #dc2626 !important;
            }
            
            .stInfo {
                border-left: 4px solid #3b82f6;
                background-color: #eff6ff;
                color: #1d4ed8 !important;
            }
            
            .stWarning {
                border-left: 4px solid #f59e0b;
                background-color: #fffbeb;
                color: #d97706 !important;
            }
            
            /* Metrics */
            .metric-container {
                background-color: #f8f9fa;
                padding: 1rem;
                border-radius: 0.3rem;
                color: #262730 !important;
            }
            
            /* Ensure all metric text is dark */
            [data-testid="metric-container"] {
                color: #262730 !important;
            }
            
            [data-testid="metric-container"] > div {
                color: #262730 !important;
            }
            
            /* Force all text in main content to be dark */
            .main .block-container {
                color: #262730 !important;
            }
            
            .main .block-container * {
                color: inherit !important;
            }
            
            /* Override any remaining white text */
            .main .block-container h1,
            .main .block-container h2,
            .main .block-container h3,
            .main .block-container h4,
            .main .block-container h5,
            .main .block-container h6,
            .main .block-container p,
            .main .block-container div,
            .main .block-container span {
                color: #262730 !important;
            }
        </style>
        """, unsafe_allow_html=True)


def render_theme_selector(language='en'):
    """Render theme selector in sidebar"""
    from translations import get_text
    
    st.markdown(get_text('theme', language))
    
    # Get current theme for proper selection
    current_theme = ThemeManager.get_current_theme()
    available_themes = ThemeManager.get_available_themes()
    
    # Create display options
    theme_options = [get_text('light', language), get_text('dark', language)]
    
    # Map display names to theme keys
    display_to_key = {
        get_text('light', language): 'light',
        get_text('dark', language): 'dark'
    }
    
    # Get current display name
    current_display = get_text(current_theme, language)
    current_index = theme_options.index(current_display) if current_display in theme_options else 0
    
    # Theme selector
    selected_display = st.selectbox(
        get_text('choose_theme', language), 
        theme_options,
        index=current_index,
        help="Switch between light and dark themes"
    )
    
    # Apply theme if changed
    selected_theme = display_to_key[selected_display]
    if selected_theme != current_theme:
        ThemeManager.set_theme(selected_theme)
        st.rerun()
