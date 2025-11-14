"""
Fluent Design System theme for Streamlit - PERMANENT DARK MODE
All backgrounds are black/dark, text is white for contrast.
"""
import streamlit as st
#Teste

def get_fluent_theme() -> str:
    """
    Get Fluent Design System CSS styles with permanent dark mode.
    
    Returns:
        CSS string with dark Fluent-inspired styling
    """
    # Dark mode colors (permanent)
    colors = {
        "bg_main": "#000000",          # Pure black main background
        "bg_card": "#1a1a1a",          # Dark card background
        "bg_secondary": "#0f0f0f",     # Secondary dark background
        "bg_input": "#2d2d2d",         # Input fields dark background
        "text_primary": "#ffffff",     # White primary text
        "text_secondary": "#e0e0e0",   # Light gray secondary text
        "text_disabled": "#808080",    # Gray disabled text
        "border": "#333333",           # Dark border
        "border_hover": "#4da6ff",     # Blue border on hover
        "brand_primary": "#4da6ff",    # Light blue brand color
        "brand_hover": "#66b3ff",      # Lighter blue on hover
        "success_bg": "#1b3d1b",       # Dark green success background
        "success_border": "#4caf50",   # Green success border
        "success_text": "#4caf50",     # Green success text
        "error_bg": "#3d1b1b",         # Dark red error background
        "error_border": "#f44336",     # Red error border
        "error_text": "#f44336",       # Red error text
        "info_bg": "#1b2d3d",          # Dark blue info background
        "info_border": "#4da6ff",      # Blue info border
        "info_text": "#4da6ff",        # Blue info text
    }
    
    return f"""
    <style>
    /* ============== FLUENT DESIGN SYSTEM - DARK MODE PERMANENT ============== */
    
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    * {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}
    
    /* Main container - pure black */
    .main {{
        background: {colors['bg_main']} !important;
        padding: 2rem;
    }}
    
    /* All text elements - white for contrast */
    h1, h2, h3, h4, h5, h6, p, span, div, label, li, td, th, a {{
        color: {colors['text_primary']} !important;
    }}
    
    /* Sidebar - dark gradient */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #1a1a1a 0%, #000000 100%) !important;
}}

[data-testid="stSidebar"] * {{
    color: #ffffff !important;
}}
    
    [data-testid="stSidebar"] * {{
        color: #ffffff !important;
    }}
    
    /* Cards - dark with white text */
    .fluent-card {{
        background: {colors['bg_card']} !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 6.4px 14.4px rgba(0, 0, 0, 0.5);
        border: 1px solid {colors['border']};
        transition: all 0.3s ease;
        min-height: 80px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }}
    
    .fluent-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 12.8px 28.8px rgba(0, 0, 0, 0.6);
        border-color: {colors['brand_primary']};
    }}
    
    /* Action cards */
    .action-card {{
        background: {colors['bg_card']} !important;
        border: 2px solid {colors['brand_primary']};
        border-radius: 8px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }}
    
    .action-card:hover {{
        transform: translateY(-6px);
        box-shadow: 0 12.8px 28.8px rgba(0, 0, 0, 0.5);
        border-color: {colors['brand_hover']};
    }}
    
    /* Buttons - blue with white text */
    .stButton > button {{
        background: #6c757d !important;         /* fundo cinza elegante */
        color: #ffffff !important;              /* texto branco */
        border: none !important;
        border-radius: 6px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.08) !important;
        transition: background 0.12s ease, transform 0.06s ease !important;
    }}
    
    .stButton > button:hover {{
        background: #5a6268 !important;
    }}
    
    .stButton > button:active {{
        background: #495057 !important;
        transform: translateY(1px) !important;
    }}
    
    .stButton > button:focus {{
        outline: none !important;
        box-shadow: 0 0 0 4px rgba(108,117,125,0.12) !important; /* halo suave */
    }}
    
    /* ===== NUMBER INPUTS ===== */
    .stNumberInput > div > div > input {{
        background: {colors['bg_input']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 4px !important;
        padding: 8px 12px !important;
    }}
    
    .stNumberInput > div {{
        background: transparent !important;
    }}
    
    .stNumberInput > div > div {{
        background: {colors['bg_input']} !important;
    }}
    
    .stNumberInput button {{
        background: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
    }}
    
    .stNumberInput button:hover {{
        background: {colors['border']} !important;
    }}
    
    .stNumberInput > div > div > input:focus {{
        border-color: {colors['brand_primary']} !important;
        box-shadow: 0 0 0 1px {colors['brand_primary']} !important;
    }}
    
    /* ===== TEXT INPUTS ===== */
    .stTextInput > div > div > input {{
        background: {colors['bg_input']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
        border-radius: 4px !important;
        padding: 8px 12px !important;
    }}
    
    .stTextInput > div {{
        background: transparent !important;
    }}
    
    .stTextInput > div > div > input:focus {{
        border-color: {colors['brand_primary']} !important;
        box-shadow: 0 0 0 1px {colors['brand_primary']} !important;
    }}
    
    /* ===== LABELS - white text ===== */
    label {{
        background: transparent !important;
        color: {colors['text_primary']} !important;
        font-weight: 600 !important;
    }}
    
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] > div,
    [data-testid="stWidgetLabel"] p {{
        background: transparent !important;
        color: {colors['text_primary']} !important;
    }}
    
    /* ===== COLUMNS ===== */
    [data-testid="column"],
    [data-testid="column"] > div {{
        background: transparent !important;
    }}
    
    /* ===== SELECT BOX ===== */
    .stSelectbox > div > div,
    .stSelectbox > div > div > div {{
        background: {colors['bg_input']} !important;
        color: {colors['text_primary']} !important;
        border: 1px solid {colors['border']} !important;
    }}
    
    [data-baseweb="select"] > div,
    [role="option"] {{
        background: {colors['bg_input']} !important;
        color: {colors['text_primary']} !important;
    }}
    
    [role="option"]:hover {{
        background: {colors['bg_secondary']} !important;
    }}
    
    /* ===== FORMS ===== */
    [data-testid="stForm"] {{
        background: {colors['bg_card']} !important;
        padding: 24px !important;
        border-radius: 8px !important;
        border: 1px solid {colors['border']} !important;
    }}
    
    /* ===== METRICS ===== */
    [data-testid="stMetric"] {{
        background: {colors['bg_secondary']} !important;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid {colors['brand_primary']};
    }}
    
    [data-testid="stMetricLabel"] {{
        color: {colors['text_secondary']} !important;
        font-size: 12px !important;
    }}
    
    [data-testid="stMetricValue"] {{
        color: {colors['text_primary']} !important;
        font-size: 28px !important;
        font-weight: 700 !important;
    }}
    
    /* ===== ALERTS ===== */
    .stSuccess {{
        background: {colors['success_bg']} !important;
        border-left: 4px solid {colors['success_border']} !important;
        color: {colors['success_text']} !important;
    }}
    
    .stError {{
        background: {colors['error_bg']} !important;
        border-left: 4px solid {colors['error_border']} !important;
        color: {colors['error_text']} !important;
    }}
    
    .stInfo {{
        background: {colors['info_bg']} !important;
        border-left: 4px solid {colors['info_border']} !important;
        color: {colors['info_text']} !important;
    }}
    
    /* ===== TABLES ===== */
    .dataframe {{
        background: {colors['bg_card']} !important;
    }}
    
    .dataframe thead th {{
        background: {colors['brand_primary']} !important;
        color: #ffffff !important;
    }}
    
    .dataframe tbody td {{
        color: {colors['text_primary']} !important;
        background: {colors['bg_card']} !important;
    }}
    
    .dataframe tbody tr:hover {{
        background: {colors['bg_secondary']} !important;
    }}
    
    /* ===== DIVIDER ===== */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, {colors['border']}, transparent);
        margin: 24px 0;
    }}
    
    /* ===== PLACEHOLDER ===== */
    input::placeholder {{
        color: {colors['text_disabled']} !important;
    }}
    
    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {{
        background: {colors['bg_card']} !important;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        color: {colors['text_secondary']} !important;
    }}
    
    .stTabs [aria-selected="true"] {{
        color: {colors['brand_primary']} !important;
        border-bottom-color: {colors['brand_primary']} !important;
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background: {colors['bg_secondary']} !important;
        color: {colors['text_primary']} !important;
        border-left: 4px solid {colors['brand_primary']};
    }}
    
    </style>
    """


def apply_fluent_theme():
    """
    Apply permanent dark Fluent Design theme.
    No parameters needed - always dark mode.
    """
    # Get dark theme CSS
    css_styles = get_fluent_theme()
    
    # Apply CSS to Streamlit app
    st.markdown(css_styles, unsafe_allow_html=True)