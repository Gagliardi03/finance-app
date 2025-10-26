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
                date_val = row["date"] if "date" in row and pd.notnull(row["date"]) else "-"
                st.text(str(date_val)[:10] if date_val != "-" else "-")

            with col2:
                st.markdown(f"**🏷️ Category**")
                cat_val = row["category"] if "category" in row and pd.notnull(row["category"]) and row["category"] != "" else "-"
                st.text(cat_val)

            with col3:
                st.markdown(f"**📍 Location**")
                st.text(row["location"] if "location" in row and row["location"] not in [None, "", "nan"] else "-")

            with col4:
                st.markdown(f"**💵 Price**")
                price_val = row["price"] if "price" in row and pd.notnull(row["price"]) else None
                st.text(f"R$ {price_val:,.2f}" if price_val is not None else "-")

            with col5:
                st.markdown(f"**💳 Payment**")
                pay_val = row["payment_method"] if "payment_method" in row and pd.notnull(row["payment_method"]) and row["payment_method"] != "" else "-"
                st.text(pay_val)

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
                date_val = row["date"] if "date" in row and pd.notnull(row["date"]) else "-"
                st.text(str(date_val)[:10] if date_val != "-" else "-")

            with col2:
                st.markdown(f"**👨‍🎓 Student**")
                student_val = row["student_name"] if "student_name" in row and pd.notnull(row["student_name"]) and row["student_name"] != "" else "-"
                st.text(student_val)

            with col3:
                st.markdown(f"**💵 Value**")
                value_val = row["class_value"] if "class_value" in row and pd.notnull(row["class_value"]) else None
                st.text(f"R$ {value_val:,.2f}" if value_val is not None else "-")

            with col4:
                st.markdown(f"**📊 Quantity**")
                qty_val = row["quantity"] if "quantity" in row and pd.notnull(row["quantity"]) else None
                st.text(f"{qty_val} classes" if qty_val is not None else "0 classes")

            with col5:
                st.markdown(f"**💰 Total**")
                total_val = row["total"] if "total" in row and pd.notnull(row["total"]) else None
                st.text(f"R$ {total_val:,.2f}" if total_val is not None else "-")

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

    st.markdown

    # Display as cards instead of table for better UX
    for idx, row in df.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])

            student_val = row["student_name"] if "student_name" in row and pd.notnull(row["student_name"]) and row["student_name"] != "" else "-"
            total_classes_val = int(row["total_classes"]) if "total_classes" in row and pd.notnull(row["total_classes"]) else 0
            total_revenue_val = row["total_revenue"] if "total_revenue" in row and pd.notnull(row["total_revenue"]) else 0

            with col1:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <p style="color: #e0e0e0; font-size: 0.875rem; margin: 0;">Student</p>
                        <h3 style="color: #ffffff; margin: 0.25rem 0;">{student_val}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #e0e0e0; font-size: 0.75rem; margin: 0;">Classes</p>
                        <p style="color: #4da6ff; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            {total_classes_val}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #e0e0e0; font-size: 0.75rem; margin: 0;">Revenue</p>
                        <p style="color: #4caf50; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            R$ {total_revenue_val:,.2f}
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
        total_val = row["total"] if "total" in row and pd.notnull(row["total"]) else 0
        category_val = row["category"] if "category" in row and pd.notnull(row["category"]) and row["category"] != "" else "-"
        percentage = (total_val / total * 100) if total > 0 else 0

        with st.container():
            col1, col2, col3 = st.columns([3, 2, 2])

            with col1:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <p style="color: #e0e0e0; font-size: 0.875rem; margin: 0;">Category</p>
                        <h3 style="color: #ffffff; margin: 0.25rem 0;">{category_val}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #e0e0e0; font-size: 0.75rem; margin: 0;">Amount</p>
                        <p style="color: #f44336; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            R$ {total_val:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div class="fluent-card" style="text-align: center;">
                        <p style="color: #e0e0e0; font-size: 0.75rem; margin: 0;">Percentage</p>
                        <p style="color: #4da6ff; font-size: 1.5rem; font-weight: 700; margin: 0;">
                            {percentage:.1f}%
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
