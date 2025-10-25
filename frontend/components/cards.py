import streamlit as st
from typing import Optional, Callable


def metric_card(
    title: str, value: str, delta: Optional[str] = None, icon: str = "📊"
) -> None:
    """
    Display a metric card with Fluent design.

    Args:
        title: Card title/label
        value: Main metric value to display
        delta: Optional delta value (e.g., "+10%")
        icon: Emoji icon for visual appeal
    """
    # Create metric with icon
    st.markdown(
        f"""
        <div class="fluent-card" style="background: #fff !important;">
            <div style="display: flex; align-items: center; gap: 1rem;">
                <span style="font-size: 2rem;">{icon}</span>
                <div>
                    <p style="color: #000; font-size: 0.875rem; font-weight: 600; margin: 0;">
                        {title}
                    </p>
                    <p style="color: #000; font-size: 2rem; font-weight: 700; margin: 0;">
                        {value}
                    </p>
                    {f'<p style=\"color: #107c10; font-size: 0.875rem; margin: 0;\">{delta}</p>' if delta else ''}
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
    with st.container():
        st.markdown(
            f"""
            <div class="fluent-card">
                <div style="text-align: center;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">{icon}</div>
                    <h3 style="color: #323130; margin-bottom: 0.5rem;">{title}</h3>
                    <p style="color: #605e5c; font-size: 0.875rem; margin-bottom: 1.5rem;">
                        {description}
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Button below card
        clicked = st.button(
            button_text, key=key, use_container_width=True, on_click=on_click
        )

        return clicked


def info_card(
    title: str, content: str, card_type: str = "info", icon: str = "ℹ️"
) -> None:
    """
    Display an informational card.

    Args:
        title: Card title
        content: Card content text
        card_type: Type of card (info, success, warning, error)
        icon: Emoji icon
    """
    # Define colors based on type
    colors = {
        "info": {"bg": "#e8f4fd", "border": "#0078d4", "text": "#0078d4"},
        "success": {"bg": "#dff6dd", "border": "#107c10", "text": "#107c10"},
        "warning": {"bg": "#fff4ce", "border": "#f7630c", "text": "#f7630c"},
        "error": {"bg": "#fde7e9", "border": "#d13438", "text": "#d13438"},
    }

    color = colors.get(card_type, colors["info"])

    st.markdown(
        f"""
        <div style="
            background: {color['bg']};
            border-left: 4px solid {color['border']};
            border-radius: 4px;
            padding: 1rem 1.5rem;
            margin: 1rem 0;
        ">
            <div style="display: flex; align-items: start; gap: 1rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <div>
                    <p style="color: {color['text']}; font-weight: 600; margin: 0 0 0.5rem 0;">
                        {title}
                    </p>
                    <p style="color: #323130; font-size: 0.875rem; margin: 0;">
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

    Args:
        label: Stat label
        value: Stat value
        subtitle: Optional subtitle text
    """
    st.markdown(
        f"""
        <div class="fluent-card" style="text-align: center;">
            <p style="color: #605e5c; font-size: 0.75rem; font-weight: 600; 
                      text-transform: uppercase; letter-spacing: 1px; margin: 0;">
                {label}
            </p>
            <p style="color: #0078d4; font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">
                {value}
            </p>
            {f'<p style="color: #8a8886; font-size: 0.875rem; margin: 0;">{subtitle}</p>' if subtitle else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def header_with_icon(text: str, icon: str = "📊", level: int = 1) -> None:
    """
    Display a header with an icon.

    Args:
        text: Header text
        icon: Emoji icon
        level: Header level (1-3)
    """
    sizes = {1: "2.5rem", 2: "2rem", 3: "1.5rem"}
    size = sizes.get(level, "2rem")

    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 1rem; margin: 2rem 0 1rem 0;">
            <span style="font-size: {size};">{icon}</span>
            <h{level} style="margin: 0;">{text}</h{level}>
        </div>
        """,
        unsafe_allow_html=True,
    )
