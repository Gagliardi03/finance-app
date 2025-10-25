import streamlit as st
from typing import Optional, Callable


def metric_card(
    title: str, value: str, delta: Optional[str] = None, icon: str = "📊"
) -> None:
    """
    Display a metric card with dark Fluent design.
    Works with permanent dark mode.

    Args:
        title: Card title/label
        value: Main metric value to display
        delta: Optional delta value (e.g., "+10%")
        icon: Emoji icon for visual appeal
    """
    # Build delta HTML only if delta exists
    if delta:
        delta_section = f'<p style="color: #4caf50; font-size: 0.875rem; margin: 0;">{delta}</p>'
    else:
        delta_section = ''
    
    st.markdown(
        f"""
        <div class="fluent-card">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 2rem;">{icon}</span>
                <div style="flex: 1;">
                    <p style="color: #e0e0e0; font-size: 0.875rem; font-weight: 600; margin: 0;">
                        {title}
                    </p>
                    <p style="color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0;">
                        {value}
                    </p>{delta_section}
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )



def action_card(
    title: str,
    description: str,
    button_text: str,
    icon: str = "📌",
    on_click: Optional[Callable] = None,
    key: Optional[str] = None,
) -> bool:
    """
    Display an interactive action card with button.
    Works with both light and dark mode.

    Args:
        title: Card title
        description: Card description text
        button_text: Text for the action button
        icon: Emoji icon
        on_click: Callback function when button is clicked
        key: Unique key for the button

    Returns:
        True if button was clicked
    """
    # Get current theme colors
    is_dark = st.session_state.get("dark_mode", False)
    text_primary = "#ffffff" if is_dark else "#242424"
    text_secondary = "#b0b0b0" if is_dark else "#605e5c"
    
    with st.container():
        st.markdown(
            f"""
            <div class="action-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                    <h3 style="color: {text_primary}; margin-bottom: 0.5rem; font-size: 18px; font-weight: 600;">
                        {title}
                    </h3>
                    <p style="color: {text_secondary}; font-size: 0.875rem; margin-bottom: 0;">
                        {description}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        clicked = st.button(
            button_text, key=key, use_container_width=True, on_click=on_click
        )

        return clicked


def info_card(
    title: str, content: str, card_type: str = "info", icon: str = "ℹ️"
) -> None:
    """
    Display an informational card.
    Works with both light and dark mode.

    Args:
        title: Card title
        content: Card content text
        card_type: Type of card (info, success, warning, error)
        icon: Emoji icon
    """
    is_dark = st.session_state.get("dark_mode", False)
    
    if is_dark:
        colors = {
            "info": {"bg": "#1b2d3d", "border": "#4da6ff", "text": "#4da6ff"},
            "success": {"bg": "#1b3d1b", "border": "#4caf50", "text": "#4caf50"},
            "warning": {"bg": "#3d2d1b", "border": "#ff9800", "text": "#ff9800"},
            "error": {"bg": "#3d1b1b", "border": "#f44336", "text": "#f44336"},
        }
        text_content = "#ffffff"
    else:
        colors = {
            "info": {"bg": "#e8f4fd", "border": "#0078d4", "text": "#0078d4"},
            "success": {"bg": "#dff6dd", "border": "#107c10", "text": "#107c10"},
            "warning": {"bg": "#fff4ce", "border": "#f7630c", "text": "#8a5700"},
            "error": {"bg": "#fde7e9", "border": "#d13438", "text": "#d13438"},
        }
        text_content = "#242424"

    color = colors.get(card_type, colors["info"])

    st.markdown(
        f"""
        <div style="background: {color['bg']}; border-left: 4px solid {color['border']}; 
                    border-radius: 4px; padding: 1rem 1.5rem; margin: 1rem 0;">
            <div style="display: flex; align-items: start; gap: 1rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div style="flex: 1;">
                    <p style="color: {color['text']}; font-weight: 600; margin: 0 0 0.5rem 0; font-size: 14px;">
                        {title}
                    </p>
                    <p style="color: {text_content}; font-size: 0.875rem; margin: 0;">
                        {content}
                    </p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def stat_card(label: str, value: str, subtitle: Optional[str] = None) -> None:
    """
    Display a simple statistics card.
    Works with both light and dark mode.

    Args:
        label: Stat label
        value: Stat value
        subtitle: Optional subtitle text
    """
    is_dark = st.session_state.get("dark_mode", False)
    text_secondary = "#b0b0b0" if is_dark else "#605e5c"
    text_disabled = "#808080" if is_dark else "#8a8886"
    brand_color = "#4da6ff" if is_dark else "#0078d4"
    
    if subtitle:
        subtitle_html = f'<p style="color: {text_disabled}; font-size: 0.875rem; margin: 0;">{subtitle}</p>'
    else:
        subtitle_html = ''
    
    st.markdown(
        f"""
        <div class="fluent-card" style="text-align: center;">
            <p style="color: {text_secondary}; font-size: 0.75rem; font-weight: 600; 
                      text-transform: uppercase; letter-spacing: 1px; margin: 0;">
                {label}
            </p>
            <p style="color: {brand_color}; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">
                {value}
            </p>{subtitle_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_with_icon(text: str, icon: str = "📊", level: int = 1) -> None:
    """
    Display a header with an icon.
    Works with both light and dark mode.

    Args:
        text: Header text
        icon: Emoji icon
        level: Header level (1-3)
    """
    sizes = {1: "2.5rem", 2: "2rem", 3: "1.5rem"}
    size = sizes.get(level, "2rem")
    
    is_dark = st.session_state.get("dark_mode", False)
    text_color = "#ffffff" if is_dark else "#242424"

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin: 2rem 0 1rem 0;">
            <span style="font-size: {size};">{icon}</span>
            <h{level} style="margin: 0; color: {text_color}; font-weight: 700;">{text}</h{level}>
        </div>
        """,
        unsafe_allow_html=True,
    )