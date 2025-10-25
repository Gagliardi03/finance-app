import streamlit as st
from typing import Optional, List, Dict, Any


def expense_form(on_submit: callable) -> None:
    """
    Display a form for adding expenses.

    Args:
        on_submit: Callback function when form is submitted
                   Should accept (category, location, price, payment_method, installments)
    """
    st.markdown("### ➕ Add New Expense")

    with st.form("expense_form", clear_on_submit=True):
        col1, col2 = st.columns(2)

        with col1:
            # Category input
            category = st.text_input(
                "Category",
                placeholder="e.g., Pharmacy, Food, Transport",
                help="What type of expense?",
            )

            # Location input
            location = st.text_input(
                "Location",
                placeholder="e.g., DROGARIA PAULISTA",
                help="Where did you spend?",
            )

            # Price input
            price = st.number_input(
                "Price (BRL)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                help="Amount spent",
            )

        with col2:
            # Payment method selection
            payment_method = st.selectbox(
                "Payment Method",
                options=["Credit Card", "Debit Card", "PIX", "Cash", "Bank Transfer"],
                help="How did you pay?",
            )

            # Installments (only for credit card)
            if payment_method == "Credit Card":
                installments = st.number_input(
                    "Installments",
                    min_value=1,
                    max_value=24,
                    value=1,
                    step=1,
                    help="Number of installments",
                )
            else:
                installments = 1
                st.info("💡 Installments only for Credit Card")

            # Empty space for alignment
            st.write("")

        # Submit button
        submitted = st.form_submit_button("💾 Save Expense", use_container_width=True)

        if submitted:
            # Validate inputs
            if not category or not location:
                st.error("❌ Please fill in all fields!")
            else:
                try:
                    # Call the callback function
                    on_submit(category, location, price, payment_method, installments)
                    st.success("✅ Expense added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def class_form(on_submit: callable) -> None:
    """
    Display a form for adding English classes.

    Args:
        on_submit: Callback function when form is submitted
                   Should accept (student_name, class_value, quantity)
    """
    st.markdown("### 📚 Register Class")

    with st.form("class_form", clear_on_submit=True):
        # Student name
        student_name = st.text_input(
            "Student Name",
            placeholder="e.g., John Smith",
            help="Name of the student",
        )

        col1, col2 = st.columns(2)

        with col1:
            # Class value
            class_value = st.number_input(
                "Class Value (BRL)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                help="Price per class",
            )

        with col2:
            # Quantity
            quantity = st.number_input(
                "Number of Classes",
                min_value=1,
                step=1,
                value=1,
                help="How many classes?",
            )

        # Show total
        total = class_value * quantity
        st.info(f"💰 **Total Amount**: R$ {total:,.2f}")

        # Submit button
        submitted = st.form_submit_button("💾 Save Classes", use_container_width=True)

        if submitted:
            # Validate inputs
            if not student_name or not student_name.strip():
                st.error("❌ Please enter student name!")
            else:
                try:
                    # Call the callback function
                    on_submit(student_name, class_value, quantity)
                    st.success(f"✅ {quantity} class(es) for {student_name} added!")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")


def filter_form(filter_options: List[str], default_option: Optional[str] = None) -> str:
    """
    Display a filter form with dropdown selection.

    Args:
        filter_options: List of options to filter by
        default_option: Default selected option

    Returns:
        Selected filter option
    """
    with st.form("filter_form"):
        col1, col2 = st.columns([3, 1])

        with col1:
            selected = st.selectbox(
                "Filter by",
                options=filter_options,
                index=(
                    filter_options.index(default_option)
                    if default_option in filter_options
                    else 0
                ),
            )

        with col2:
            st.write("")  # Spacing
            st.write("")  # Spacing
            submitted = st.form_submit_button("Apply", use_container_width=True)

        if submitted:
            return selected

        return selected


def search_form(placeholder: str = "Search...") -> Optional[str]:
    """
    Display a search form.

    Args:
        placeholder: Placeholder text for search input

    Returns:
        Search query string or None
    """
    with st.form("search_form"):
        col1, col2 = st.columns([4, 1])

        with col1:
            query = st.text_input(
                "Search", placeholder=placeholder, label_visibility="collapsed"
            )

        with col2:
            submitted = st.form_submit_button("🔍", use_container_width=True)

        if submitted and query:
            return query

        return None


def date_range_form() -> tuple:
    """
    Display a date range selection form.

    Returns:
        Tuple of (start_date, end_date)
    """
    with st.form("date_range_form"):
        col1, col2, col3 = st.columns([2, 2, 1])

        with col1:
            start_date = st.date_input("Start Date")

        with col2:
            end_date = st.date_input("End Date")

        with col3:
            st.write("")  # Spacing
            st.write("")  # Spacing
            submitted = st.form_submit_button("Filter", use_container_width=True)

        if submitted:
            return start_date, end_date

        return None, None
