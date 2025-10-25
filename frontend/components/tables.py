import streamlit as st
import pandas as pd
from typing import Optional, Callable, List


def expense_table(
    df: pd.DataFrame, on_delete: Optional[Callable[[int], None]] = None
) -> None:
    """
    Display expenses in a formatted table with delete option.

    Args:
        df: DataFrame with expense data
        on_delete: Optional callback function for delete action
    """
    if df.empty:
        st.info("📭 No expenses registered yet")
        return

    st.markdown("### 📋 Expense List")

    # Display each expense as a row
    for idx, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

            with col1:
                st.markdown(f"**📅 Date**")
                st.text(row["date"][:10])

            with col2:
                st.markdown(f"**🏷️ Category**")
                st.text(row["category"])

            with col3:
                st.markdown(f"**📍 Location**")
                st.text(row["location"])

            with col4:
                st.markdown(f"**💵 Price**")
                st.text(f"R$ {row['price']:,.2f}")

            with col5:
                st.markdown(f"**💳 Payment**")
                st.text(row["payment_method"])

            with col6:
                if on_delete:
                    if st.button(
                        "🗑️", key=f"del_exp_{row['id']}", help="Delete expense",
                        use_container_width=False,
                        args=(),
                        kwargs=None,
                        type="primary"
                    ):
                        try:
                            on_delete(row["id"])
                            st.success("✅ Deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            st.divider()


def class_table(
    df: pd.DataFrame, on_delete: Optional[Callable[[int], None]] = None
) -> None:
    """
    Display classes in a formatted table with delete option.

    Args:
        df: DataFrame with class data
        on_delete: Optional callback function for delete action
    """
    if df.empty:
        st.info("📭 No classes registered yet")
        return

    st.markdown("### 📚 Class List")

    # Display each class as a row
    for idx, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5, col6 = st.columns([2, 2, 2, 2, 2, 1])

            with col1:
                st.markdown(f"**📅 Date**")
                st.text(row["date"][:10])

            with col2:
                st.markdown(f"**👨‍🎓 Student**")
                st.text(row["student_name"])

            with col3:
                st.markdown(f"**💵 Value**")
                st.text(f"R$ {row['class_value']:,.2f}")

            with col4:
                st.markdown(f"**📊 Quantity**")
                st.text(f"{row['quantity']} classes")

            with col5:
                st.markdown(f"**💰 Total**")
                st.text(f"R$ {row['total']:,.2f}")

            with col6:
                if on_delete:
                    if st.button(
                        "🗑️", key=f"del_cls_{row['id']}", help="Delete class",
                        use_container_width=False,
                        args=(),
                        kwargs=None,
                        type="primary"
                    ):
                        try:
                            on_delete(row["id"])
                            st.success("✅ Deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error: {e}")

            st.divider()


def summary_table(df: pd.DataFrame, title: str = "Summary") -> None:
    """
    Display a summary table with styled dataframe.

    Args:
        df: DataFrame to display
        title: Table title
    """
    if df.empty:
        st.info("📭 No data available")
        return

    st.markdown(f"### {title}")

    # Style the dataframe
    styled_df = df.style.format(
        {
            col: "R$ {:,.2f}"
            for col in df.columns
            if df[col].dtype in ["float64", "float32"]
        }
    )

    st.dataframe(styled_df, use_container_width=True)


def student_summary_table(df: pd.DataFrame) -> None:
    """
    Display student revenue summary table.

    Args:
        df: DataFrame with student summary data
    """
    if df.empty:
        st.info("📭 No student data available")
        return

    st.markdown("### 👨‍🎓 Student Revenue Summary")

    # Display as cards instead of table for better UX
    for idx, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <p style="color: #605e5c; font-size: 0.875rem; margin: 0;">Student</p>
                        <h3 style="color: #323130; margin: 0.25rem 0;">{row['student_name']}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #605e5c; font-size: 0.75rem; margin: 0;">Classes</p>
                        <p style="color: #0078d4; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            {int(row['total_classes'])}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #605e5c; font-size: 0.75rem; margin: 0;">Revenue</p>
                        <p style="color: #107c10; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            R$ {row['total_revenue']:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)


def category_summary_table(df: pd.DataFrame) -> None:
    """
    Display category spending summary table.

    Args:
        df: DataFrame with category summary data
    """
    if df.empty:
        st.info("📭 No category data available")
        return

    st.markdown("### 🏷️ Spending by Category")

    # Calculate total for percentage
    total = df["total"].sum()

    # Display as cards
    for idx, row in df.iterrows():
        percentage = (row["total"] / total * 100) if total > 0 else 0

        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <p style="color: #605e5c; font-size: 0.875rem; margin: 0;">Category</p>
                        <h3 style="color: #323130; margin: 0.25rem 0;">{row['category']}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #605e5c; font-size: 0.75rem; margin: 0;">Amount</p>
                        <p style="color: #d13438; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            R$ {row['total']:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #605e5c; font-size: 0.75rem; margin: 0;">Percentage</p>
                        <p style="color: #0078d4; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            {percentage:.1f}%
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
