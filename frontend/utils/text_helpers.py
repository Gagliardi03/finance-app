"""
Text rendering helper functions for consistent typography.
Use these functions to render text elements throughout the application.
"""

import streamlit as st
from typing import Optional
from frontend.utils.typography import (
    TITLE_SIZE,
    TITLE_WEIGHT,
    HEADING_SIZE,
    HEADING_WEIGHT,
    SUBHEADING_SIZE,
    SUBHEADING_WEIGHT,
    CARD_TITLE_SIZE,
    CARD_TITLE_WEIGHT,
    BODY_SIZE,
    BODY_WEIGHT,
    SMALL_SIZE,
    SMALL_WEIGHT,
    TINY_SIZE,
    TINY_WEIGHT,
    METRIC_SIZE,
    METRIC_WEIGHT,
    NUMBER_SIZE,
    NUMBER_WEIGHT,
    SMALL_NUMBER_SIZE,
    SMALL_NUMBER_WEIGHT,
    TEXT_PRIMARY,
    TEXT_SECONDARY,
    TEXT_TERTIARY,
    TEXT_DISABLED,
    TEXT_MUTED,
    SPACING_SM,
    SPACING_MD,
    SPACING_LG,
    LINE_HEIGHT_NORMAL,
    LINE_HEIGHT_TIGHT,
    LETTER_SPACING_NORMAL,
    LETTER_SPACING_WIDE,
)


def render_title(
    text: str, icon: Optional[str] = None, margin_bottom: str = SPACING_LG
) -> None:
    """
    Render a main page title.

    Args:
        text: Title text
        icon: Optional emoji icon
        margin_bottom: Bottom margin (default: 24px)

    Example:
        render_title("Financial Dashboard", icon="💰")
    """
    icon_html = (
        f'<span style="margin-right: {SPACING_MD};">{icon}</span>' if icon else ""
    )

    st.markdown(
        f"""
        <h1 style="font-size: {TITLE_SIZE}; 
                   font-weight: {TITLE_WEIGHT}; 
                   color: {TEXT_PRIMARY}; 
                   margin: 0 0 {margin_bottom} 0;
                   line-height: {LINE_HEIGHT_TIGHT};">
            {icon_html}{text}
        </h1>
        """,
        unsafe_allow_html=True,
    )


def render_heading(
    text: str, icon: Optional[str] = None, margin_bottom: str = SPACING_MD
) -> None:
    """
    Render a section heading.

    Args:
        text: Heading text
        icon: Optional emoji icon
        margin_bottom: Bottom margin (default: 16px)

    Example:
        render_heading("Quick Stats", icon="📊")
    """
    icon_html = (
        f'<span style="margin-right: {SPACING_SM};">{icon}</span>' if icon else ""
    )

    st.markdown(
        f"""
        <h2 style="font-size: {HEADING_SIZE}; 
                   font-weight: {HEADING_WEIGHT}; 
                   color: {TEXT_PRIMARY}; 
                   margin: 0 0 {margin_bottom} 0;
                   line-height: {LINE_HEIGHT_TIGHT};">
            {icon_html}{text}
        </h2>
        """,
        unsafe_allow_html=True,
    )


def render_subheading(
    text: str, icon: Optional[str] = None, margin_bottom: str = SPACING_MD
) -> None:
    """
    Render a subsection heading.

    Args:
        text: Subheading text
        icon: Optional emoji icon
        margin_bottom: Bottom margin (default: 16px)

    Example:
        render_subheading("Monthly Trends", icon="📅")
    """
    icon_html = (
        f'<span style="margin-right: {SPACING_SM};">{icon}</span>' if icon else ""
    )

    st.markdown(
        f"""
        <h3 style="font-size: {SUBHEADING_SIZE}; 
                   font-weight: {SUBHEADING_WEIGHT}; 
                   color: {TEXT_PRIMARY}; 
                   margin: 0 0 {margin_bottom} 0;
                   line-height: {LINE_HEIGHT_NORMAL};">
            {icon_html}{text}
        </h3>
        """,
        unsafe_allow_html=True,
    )


def render_card_title(text: str, color: str = TEXT_PRIMARY) -> None:
    """
    Render a card title.

    Args:
        text: Card title text
        color: Text color (default: white)

    Example:
        render_card_title("Total Expenses")
    """
    st.markdown(
        f"""
        <p style="font-size: {CARD_TITLE_SIZE}; 
                  font-weight: {CARD_TITLE_WEIGHT}; 
                  color: {color}; 
                  margin: 0;
                  line-height: {LINE_HEIGHT_NORMAL};">
            {text}
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_body(text: str, color: str = TEXT_SECONDARY) -> None:
    """
    Render body text.

    Args:
        text: Body text
        color: Text color (default: light gray)

    Example:
        render_body("Track your spending patterns and financial trends.")
    """
    st.markdown(
        f"""
        <p style="font-size: {BODY_SIZE}; 
                  font-weight: {BODY_WEIGHT}; 
                  color: {color}; 
                  margin: 0;
                  line-height: {LINE_HEIGHT_NORMAL};">
            {text}
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_small(text: str, color: str = TEXT_TERTIARY) -> None:
    """
    Render small text (descriptions, hints).

    Args:
        text: Small text
        color: Text color (default: gray)

    Example:
        render_small("Last updated 5 minutes ago")
    """
    st.markdown(
        f"""
        <p style="font-size: {SMALL_SIZE}; 
                  font-weight: {SMALL_WEIGHT}; 
                  color: {color}; 
                  margin: 0;
                  line-height: {LINE_HEIGHT_NORMAL};">
            {text}
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_tiny(text: str, color: str = TEXT_MUTED, uppercase: bool = True) -> None:
    """
    Render tiny text (labels, metadata).

    Args:
        text: Tiny text
        color: Text color (default: muted gray)
        uppercase: Whether to uppercase the text (default: True)

    Example:
        render_tiny("Total Revenue")
    """
    text_transform = "uppercase" if uppercase else "none"

    st.markdown(
        f"""
        <p style="font-size: {TINY_SIZE}; 
                  font-weight: {TINY_WEIGHT}; 
                  color: {color}; 
                  margin: 0;
                  text-transform: {text_transform};
                  letter-spacing: {LETTER_SPACING_WIDE};
                  line-height: {LINE_HEIGHT_NORMAL};">
            {text}
        </p>
        """,
        unsafe_allow_html=True,
    )


def render_metric(value: str, label: str, color: str = TEXT_PRIMARY) -> None:
    """
    Render a large metric value with label.

    Args:
        value: Metric value (e.g., "R$ 5,000.00")
        label: Metric label (e.g., "Total Revenue")
        color: Value color (default: white)

    Example:
        render_metric("R$ 5,000.00", "Total Revenue", color="#4caf50")
    """
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-size: {TINY_SIZE}; 
                      font-weight: {TINY_WEIGHT}; 
                      color: {TEXT_TERTIARY}; 
                      margin: 0 0 {SPACING_SM} 0;
                      text-transform: uppercase;
                      letter-spacing: {LETTER_SPACING_WIDE};">
                {label}
            </p>
            <p style="font-size: {METRIC_SIZE}; 
                      font-weight: {METRIC_WEIGHT}; 
                      color: {color}; 
                      margin: 0;
                      line-height: {LINE_HEIGHT_TIGHT};">
                {value}
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_number(
    value: str, label: Optional[str] = None, color: str = TEXT_PRIMARY
) -> None:
    """
    Render a medium-sized number with optional label.

    Args:
        value: Number value
        label: Optional label below the number
        color: Number color (default: white)

    Example:
        render_number("150", label="Total Classes", color="#4da6ff")
    """
    label_html = (
        f"""
        <p style="font-size: {SMALL_SIZE}; 
                  color: {TEXT_TERTIARY}; 
                  margin: {SPACING_SM} 0 0 0;">
            {label}
        </p>
    """
        if label
        else ""
    )

    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-size: {NUMBER_SIZE}; 
                      font-weight: {NUMBER_WEIGHT}; 
                      color: {color}; 
                      margin: 0;
                      line-height: {LINE_HEIGHT_TIGHT};">
                {value}
            </p>{label_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_description(text: str, icon: Optional[str] = None) -> None:
    """
    Render a description paragraph with optional icon.

    Args:
        text: Description text
        icon: Optional emoji icon

    Example:
        render_description("Manage your finances in one place", icon="💰")
    """
    icon_html = (
        f'<span style="margin-right: {SPACING_SM};">{icon}</span>' if icon else ""
    )

    st.markdown(
        f"""
        <p style="font-size: {BODY_SIZE}; 
                  font-weight: {BODY_WEIGHT}; 
                  color: {TEXT_SECONDARY}; 
                  margin: 0;
                  line-height: {LINE_HEIGHT_NORMAL};">
            {icon_html}{text}
        </p>
        """,
        unsafe_allow_html=True,
    )
