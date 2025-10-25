import streamlit as st
from backend import ExpenseService, ClassService
from frontend.components import (
    header_with_icon,
    action_card,
    metric_card,
    comparison_chart,
)


def show_home_page(expense_service: ExpenseService, class_service: ClassService):
    """
    Display home/dashboard page with overview and quick stats.

    Args:
        expense_service: Service for expense operations
        class_service: Service for class operations
    """
    # Page header
    header_with_icon("Welcome to Your Financial Dashboard", "💰", level=1)

    st.markdown(
        """
        <p style='font-size: 1.1rem; color: #605e5c; margin-bottom: 2rem;'>
            Manage your finances and track your English classes all in one place.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Quick actions section
    st.markdown("## 🚀 Quick Actions")
    col1, col2, col3 = st.columns(3)

    with col1:
        if action_card(
            title="Track Expenses",
            description="View and manage all your expenses",
            button_text="View Expenses",
            icon="📊",
            key="track_btn",
        ):
            st.session_state.page = "expenses"
            st.rerun()

    with col2:
        if action_card(
            title="Analytics",
            description="Visualize your spending patterns",
            button_text="View Analytics",
            icon="📈",
            key="analytics_btn",
        ):
            st.session_state.page = "analytics"
            st.rerun()

    with col3:
        if action_card(
            title="Class Revenue",
            description="Track your teaching revenue",
            button_text="View Classes",
            icon="🎓",
            key="classes_btn",
        ):
            st.session_state.page = "classes"
            st.rerun()

    st.divider()

    # Quick stats section
    try:
        # Get statistics
        expense_stats = expense_service.get_expense_stats()
        class_stats = class_service.get_class_stats()

        # Display metrics
        st.markdown("## 📊 Overview")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            metric_card(
                title="Total Expenses",
                value=str(expense_stats.total_expenses),
                icon="📝",
            )

        with col2:
            metric_card(
                title="Total Spent",
                value=f"R$ {expense_stats.total_spent:,.2f}",
                icon="💸",
            )

        with col3:
            metric_card(
                title="Total Classes",
                value=str(class_stats.total_classes),
                icon="📚",
            )

        with col4:
            metric_card(
                title="Class Revenue",
                value=f"R$ {class_stats.total_revenue:,.2f}",
                icon="💰",
            )

        st.divider()

        # Comparison chart
        if expense_stats.total_spent > 0 or class_stats.total_revenue > 0:
            st.markdown("## 💹 Financial Balance")

            comparison_chart(
                expenses_total=expense_stats.total_spent,
                revenue_total=class_stats.total_revenue,
                title="Expenses vs Revenue",
            )

            # Calculate balance
            balance = class_stats.total_revenue - expense_stats.total_spent

            if balance >= 0:
                st.success(
                    f"✅ **Positive Balance**: Your revenue exceeds expenses by R$ {balance:,.2f}"
                )
            else:
                st.warning(
                    f"⚠️ **Negative Balance**: Your expenses exceed revenue by R$ {abs(balance):,.2f}"
                )

        st.divider()

        # Additional insights
        st.markdown("## 💡 Insights")

        col1, col2 = st.columns(2)

        with col1:
            if expense_stats.total_expenses > 0:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <h4 style="color: #323130; margin-bottom: 1rem;">💸 Spending Insights</h4>
                        <p style="color: #605e5c; margin: 0.5rem 0;">
                            <strong>Average Expense:</strong> R$ {expense_stats.average_expense:,.2f}
                        </p>
                        <p style="color: #605e5c; margin: 0.5rem 0;">
                            <strong>Top Category:</strong> {expense_stats.top_category}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("📭 No expense data yet. Start adding expenses!")

        with col2:
            if class_stats.total_classes > 0:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <h4 style="color: #323130; margin-bottom: 1rem;">🎓 Teaching Insights</h4>
                        <p style="color: #605e5c; margin: 0.5rem 0;">
                            <strong>Total Students:</strong> {class_stats.student_count}
                        </p>
                        <p style="color: #605e5c; margin: 0.5rem 0;">
                            <strong>Average per Class:</strong> R$ {class_stats.average_per_class:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("📭 No class data yet. Start adding classes!")

    except Exception as e:
        st.error(f"❌ Error loading dashboard data: {e}")
