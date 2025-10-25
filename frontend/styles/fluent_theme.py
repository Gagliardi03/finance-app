"""
Fluent Design System theme for Streamlit.
Inspired by Microsoft Fluent UI with modern, clean aesthetics.
"""


def get_fluent_theme() -> str:
    """
    Get Fluent Design System CSS styles.

    Returns:
        CSS string with Fluent-inspired styling
    """
    return """
    <style>
    /* ============== FLUENT DESIGN SYSTEM ============== */
    
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@300;400;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
        color: #000 !important;
    }
    
    /* Main container */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
        padding: 2rem;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0078d4 0%, #005a9e 100%);
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #000 !important;
    }
    
    /* Card styling - Fluent acrylic effect */
    .fluent-card {
        background: #fff !important;
        border-radius: 8px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(0, 120, 212, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .fluent-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 120, 212, 0.15);
        border-color: rgba(0, 120, 212, 0.3);
    }
    
    /* Button styling - Fluent design */
    .stButton > button {
        background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%);
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        font-size: 14px;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 8px rgba(0, 120, 212, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #106ebe 0%, #005a9e 100%);
        box-shadow: 0 4px 16px rgba(0, 120, 212, 0.3);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0);
        box-shadow: 0 2px 8px rgba(0, 120, 212, 0.2);
    }
    
    /* Metric cards - Modern look */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        border-left: 4px solid #0078d4;
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0, 120, 212, 0.12);
    }
    
    [data-testid="stMetricLabel"] {
        color: #000 !important;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricValue"] {
        color: #000 !important;
        font-size: 32px;
        font-weight: 700;
    }
    
    /* Input fields - Fluent style */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stSelectbox > div > div > select {
        border: 2px solid #e1dfdd;
        border-radius: 4px;
        padding: 0.75rem;
        font-size: 14px;
        transition: all 0.3s ease;
        background: #fff !important;
        color: #000 !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #0078d4;
        box-shadow: 0 0 0 3px rgba(0, 120, 212, 0.1);
        outline: none;
    }
    
    /* Headers - Modern typography */
    h1 {
        color: #000 !important;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #000 !important;
        font-weight: 600;
        font-size: 1.75rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
    }
    
    h3 {
        color: #000 !important;
        font-weight: 600;
        font-size: 1.25rem;
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Info boxes - Fluent alert style */
    .stAlert {
        border-radius: 4px;
        border-left: 4px solid;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(10px);
    }
    
    /* Success message */
    [data-baseweb="notification"][kind="success"] {
        background: #dff6dd;
        border-left-color: #107c10;
        color: #107c10;
    }
    
    /* Error message */
    [data-baseweb="notification"][kind="error"] {
        background: #fde7e9;
        border-left-color: #d13438;
        color: #d13438;
    }
    
    /* Info message */
    [data-baseweb="notification"][kind="info"] {
        background: #e8f4fd;
        border-left-color: #0078d4;
        color: #0078d4;
    }
    
    /* Tables - Clean design */
    .dataframe {
        border: none !important;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
    }
    
    .dataframe thead tr {
        background: linear-gradient(135deg, #0078d4 0%, #005a9e 100%);
        color: white !important;
    }
    
    .dataframe thead th {
        padding: 1rem !important;
        font-weight: 600;
        text-align: left;
        border: none !important;
    }
    
    .dataframe tbody tr {
        border-bottom: 1px solid #f3f2f1;
        transition: background 0.2s ease;
    }
    
    .dataframe tbody tr:hover {
        background: #f8f9fa;
    }
    
    .dataframe tbody td {
        padding: 0.75rem 1rem !important;
        border: none !important;
    }
    
    /* Divider - Subtle line */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e1dfdd, transparent);
        margin: 2rem 0;
    }
    
    /* Form containers */
    [data-testid="stForm"] {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
        border: 1px solid rgba(0, 120, 212, 0.1);
    }
    
    /* Expander - Accordion style */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 4px;
        padding: 1rem;
        font-weight: 600;
        color: #000 !important;
        border-left: 4px solid #0078d4;
    }
    
    /* Column containers */
    [data-testid="column"] {
        padding: 0.5rem;
    }
    
    /* Spinner - Fluent animation */
    .stSpinner > div {
        border-color: #0078d4 !important;
        border-right-color: transparent !important;
    }
    
    /* Progress bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0078d4, #005a9e);
    }
    
    /* Toast notifications */
    .element-container {
        animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f3f2f1;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #c8c6c4;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #a19f9d;
    }
    
    /* Tooltips */
    [data-testid="stTooltipIcon"] {
        color: #0078d4;
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        border: 2px dashed #c8c6c4;
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #0078d4;
        background: rgba(0, 120, 212, 0.02);
    }
    
    </style>
    """


def apply_fluent_theme():
    """
    Apply Fluent Design System theme to Streamlit app.
    This function should be called at the start of the app.
    """
    import streamlit as st

    st.markdown(get_fluent_theme(), unsafe_allow_html=True)
