import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Optional


def expense_pie_chart(df: pd.DataFrame, title: str = "Expenses by Category") -> None:
    """
    Display pie chart of expenses by category.

    Args:
        df: DataFrame with category and total columns
        title: Chart title
    """
    if df.empty:
        st.info("📭 No data to display")
        return

    # Create pie chart with Fluent colors
    fig = px.pie(
        df,
        values="total",
        names="category",
        title=title,
        color_discrete_sequence=px.colors.qualitative.Bold,
    )

    # Update layout with Fluent styling
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", size=14),
        title_font=dict(size=20, color="#323130"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        height=400,
    )

    # Update traces for better visuals
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)


def expense_bar_chart(df: pd.DataFrame, title: str = "Expenses by Category") -> None:
    """
    Display bar chart of expenses by category.

    Args:
        df: DataFrame with category and total columns
        title: Chart title
    """
    if df.empty:
        st.info("📭 No data to display")
        return

    # Create bar chart
    fig = px.bar(
        df,
        x="category",
        y="total",
        title=title,
        color="total",
        color_continuous_scale="Blues",
        labels={"total": "Total Spent (BRL)", "category": "Category"},
    )

    # Update layout
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", size=14),
        title_font=dict(size=20, color="#323130"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=400,
        xaxis_title="Category",
        yaxis_title="Total Spent (R$)",
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)


def monthly_trend_chart(
    df: pd.DataFrame, title: str = "Monthly Trend", y_label: str = "Amount (R$)"
) -> None:
    """
    Display line chart of monthly trends.

    Args:
        df: DataFrame with month and value columns
        title: Chart title
        y_label: Y-axis label
    """
    if df.empty:
        st.info("📭 No data to display")
        return

    # Determine column names dynamically
    value_col = [col for col in df.columns if col != "month"][0]

    # Create line chart
    fig = px.line(
        df,
        x="month",
        y=value_col,
        title=title,
        markers=True,
        labels={"month": "Month", value_col: y_label},
    )

    # Update layout
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", size=14),
        title_font=dict(size=20, color="#323130"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=400,
        xaxis_title="Month",
        yaxis_title=y_label,
    )

    # Update traces with Fluent colors
    fig.update_traces(
        line_color="#0078d4",
        marker=dict(size=10, color="#0078d4", line=dict(width=2, color="white")),
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)


def payment_method_chart(
    payment_dict: dict, title: str = "Spending by Payment Method"
) -> None:
    """
    Display donut chart of spending by payment method.

    Args:
        payment_dict: Dictionary with payment_method as key and total as value
        title: Chart title
    """
    if not payment_dict:
        st.info("📭 No data to display")
        return

    # Convert dict to DataFrame
    df = pd.DataFrame(list(payment_dict.items()), columns=["method", "total"])

    # Create donut chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["method"],
                values=df["total"],
                hole=0.4,
                marker=dict(colors=px.colors.qualitative.Set3),
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title=title,
        font=dict(family="Segoe UI, sans-serif", size=14),
        title_font=dict(size=20, color="#323130"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
        height=400,
        annotations=[
            dict(
                text="Payment<br>Methods",
                x=0.5,
                y=0.5,
                font_size=16,
                showarrow=False,
                font_color="#605e5c",
            )
        ],
    )

    # Update traces
    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)


def student_revenue_chart(df: pd.DataFrame, title: str = "Revenue by Student") -> None:
    """
    Display horizontal bar chart of revenue by student.

    Args:
        df: DataFrame with student_name and total_revenue columns
        title: Chart title
    """
    if df.empty:
        st.info("📭 No data to display")
        return

    # Sort by revenue
    df_sorted = df.sort_values("total_revenue", ascending=True)

    # Create horizontal bar chart
    fig = px.bar(
        df_sorted,
        x="total_revenue",
        y="student_name",
        title=title,
        orientation="h",
        color="total_revenue",
        color_continuous_scale="Greens",
        labels={"total_revenue": "Revenue (R$)", "student_name": "Student"},
    )

    # Update layout
    fig.update_layout(
        font=dict(family="Segoe UI, sans-serif", size=14),
        title_font=dict(size=20, color="#323130"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=max(400, len(df_sorted) * 50),
        xaxis_title="Revenue (R$)",
        yaxis_title="Student",
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>R$ %{x:,.2f}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)


def comparison_chart(
    expenses_total: float, revenue_total: float, title: str = "Expenses vs Revenue"
) -> None:
    """
    Display comparison chart between expenses and revenue.

    Args:
        expenses_total: Total expenses amount
        revenue_total: Total revenue amount
        title: Chart title
    """
    # Create data
    categories = ["Expenses", "Revenue"]
    values = [expenses_total, revenue_total]
    colors = ["#d13438", "#107c10"]

    # Create bar chart
    fig = go.Figure(
        data=[
            go.Bar(
                x=categories,
                y=values,
                marker_color=colors,
                text=[f"R$ {v:,.2f}" for v in values],
                textposition="outside",
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title=title,
        font=dict(family="Segoe UI, sans-serif", size=14),
        title_font=dict(size=20, color="#323130"),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        height=400,
        yaxis_title="Amount (R$)",
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
    )

    st.plotly_chart(fig, use_container_width=True)
