import streamlit as st
from backend import ExpenseService
from frontend.components import (
    header_with_icon,
    expense_form,
    expense_table,
    metric_card,
    info_card,
)


def show_expenses_page(expense_service: ExpenseService):
    """
    Display expenses page for viewing and adding expenses.

    Args:
        expense_service: Service for expense operations
    """
    # Page header
    header_with_icon("Expense Tracker", "💸", level=1)

    # Navigation buttons
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.divider()

    # Two-column layout
    col_form, col_list = st.columns([1, 1])

    # Left column: Add expense form
    with col_form:
        st.markdown("### ➕ Add New Expense")

        # Define callback function for form submission
        def handle_expense_submit(
            category: str,
            location: str,
            price: float,
            payment_method: str,
            installments: int,
        ):
            """Handle expense form submission"""
            expense_service.create_expense(
                category=category,
                location=location,
                price=price,
                payment_method=payment_method,
                installments=installments,
            )

        # Display expense form
        expense_form(on_submit=handle_expense_submit)

        st.divider()

        # Show quick stats
        try:
            stats = expense_service.get_expense_stats()

            if stats.total_expenses > 0:
                st.markdown("### 📊 Quick Stats")

                metric_card(
                    title="Total Spent",
                    value=f"R$ {stats.total_spent:,.2f}",
                    icon="💰",
                )

                metric_card(
                    title="Average Expense",
                    value=f"R$ {stats.average_expense:,.2f}",
                    icon="📊",
                )

                metric_card(
                    title="Top Category",
                    value=stats.top_category,
                    icon="🏷️",
                )

        except Exception as e:
            st.error(f"❌ Error loading stats: {e}")

    # Right column: Expense list
    with col_list:
        st.markdown("### 📋 Your Expenses")

        try:
            # Get all expenses
            df_expenses = expense_service.get_all_expenses()

            if df_expenses.empty:
                info_card(
                    title="No Expenses Yet",
                    content="Start by adding your first expense using the form on the left.",
                    card_type="info",
                    icon="📭",
                )
            else:
                # Show total count
                st.info(f"📊 **Total Expenses**: {len(df_expenses)}")

                # Define callback for delete action
                def handle_delete(expense_id: int):
                    """Handle expense deletion"""
                    expense_service.delete_expense(expense_id)

                # Display expenses table
                expense_table(df_expenses, on_delete=handle_delete)

                # Clear all button (dangerous action)
                st.divider()

                with st.expander("⚠️ Danger Zone"):
                    st.warning("**Warning**: This action cannot be undone!")

                    col1, col2 = st.columns([1, 2])

                    with col1:
                        if st.button(
                            "🗑️ Clear All Expenses",
                            type="primary",
                            use_container_width=True,
                        ):
                            try:
                                expense_service.clear_all_expenses()
                                st.success("✅ All expenses cleared!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Error: {e}")

        except Exception as e:
            st.error(f"❌ Error loading expenses: {e}")

    st.divider()

    # Export section
    try:
        df_expenses = expense_service.get_all_expenses()

        if not df_expenses.empty:
            st.markdown("### 📥 Export Data")

            col1, col2, col3 = st.columns(3)

            with col1:
                # Export to CSV
                csv = df_expenses.to_csv(index=False)
                st.download_button(
                    label="📄 Download as CSV",
                    data=csv,
                    file_name="expenses.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            with col2:
                # Export to Excel (basic)
                from io import BytesIO

                buffer = BytesIO()
                df_expenses.to_excel(buffer, index=False, engine="openpyxl")
                buffer.seek(0)

                st.download_button(
                    label="📊 Download as Excel",
                    data=buffer,
                    file_name="expenses.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True,
                )

    except Exception as e:
        pass  # Silently fail for export section
