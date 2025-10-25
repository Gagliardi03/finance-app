import streamlit as st


def dark_mode_toggle():
    """
    Display dark mode toggle switch.
    Manages dark mode state and applies appropriate theme.
    """
    # Initialize dark mode state
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False

    # Create toggle in sidebar
    with st.sidebar:
        st.markdown("---")
        
        # Toggle button
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; gap: 0.5rem; padding: 0.5rem 0;">
                    <span style="font-size: 1.2rem;">{"🌙" if not st.session_state.dark_mode else "☀️"}</span>
                    <span style="color: #ffffff; font-weight: 600;">
                        {"Dark Mode" if not st.session_state.dark_mode else "Light Mode"}
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        with col2:
            if st.button(
                "🔄",
                key="toggle_dark_mode",
                help="Toggle dark/light mode",
                use_container_width=True,
            ):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()

    return st.session_state.dark_mode


def get_theme_colors():
    """
    Get current theme colors based on dark mode state.
    
    Returns:
        dict: Dictionary with color tokens
    """
    is_dark = st.session_state.get("dark_mode", False)
    
    if is_dark:
        # Dark mode colors
        return {
            "bg_main": "#1a1a1a",
            "bg_card": "#2d2d2d",
            "bg_secondary": "#252525",
            "text_primary": "#ffffff",
            "text_secondary": "#b0b0b0",
            "text_disabled": "#808080",
            "border": "#404040",
            "brand_primary": "#4da6ff",
            "success": "#4caf50",
            "error": "#f44336",
            "warning": "#ff9800",
        }
    else:
        # Light mode colors
        return {
            "bg_main": "#fafafa",
            "bg_card": "#ffffff",
            "bg_secondary": "#f5f5f5",
            "text_primary": "#242424",
            "text_secondary": "#605e5c",
            "text_disabled": "#8a8886",
            "border": "#e0e0e0",
            "brand_primary": "#0078d4",
            "success": "#107c10",
            "error": "#d13438",
            "warning": "#f7630c",
        }