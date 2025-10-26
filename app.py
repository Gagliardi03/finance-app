"""
Personal Finance Manager
Modern financial tracking application with Fluent Design System.

This is the main entry point of the application.
"""

import streamlit as st
from backend import FinanceDB, ExpenseService, ClassService
from frontend import (
    apply_fluent_theme,
    show_home_page,
    show_expenses_page,
    show_classes_page,
    show_analytics_page,
)


# ====================
# Page Configuration
# ====================
st.set_page_config(
    page_title="Personal Finance Manager",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ====================
# Initialize Services
# ====================
@st.cache_resource
def init_services():
    """
    Initialize database and services.
    Cached to avoid recreating on every rerun.

    Returns:
        Tuple of (ExpenseService, ClassService)
    """
    # Initialize database
    db = FinanceDB()

    # Create services
    expense_service = ExpenseService(db)
    class_service = ClassService(db)

    return expense_service, class_service


# ====================
# Sidebar Navigation
# ====================
def show_sidebar(expense_service: ExpenseService, class_service: ClassService):
    """
    Display sidebar with navigation and quick stats.

    Args:
        expense_service: Service for expense operations
        class_service: Service for class operations
    """
    with st.sidebar:
        # App title
        st.markdown(
            """
            <h1 style='text-align: center; color: white; padding: 1rem 0;'>
                💰 Finance Manager
            </h1>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # Navigation section
        st.markdown("### 📱 Navigation")

        # Home button
        if st.button("🏠 Home", use_container_width=True, key="nav_home"):
            st.session_state.page = "home"
            st.rerun()

        st.markdown("#### 💸 Finances")

        # Finance Add button - full width
        if st.button("💰 Add Expense", use_container_width=True, key="nav_add_expense"):
            st.session_state.page = "expenses"
            st.rerun()

        st.markdown("#### 🎓 Classes")

        # Classes Add button - full width
        if st.button("📚 Add Class", use_container_width=True, key="nav_add_class"):
            st.session_state.page = "classes"
            st.rerun()

        st.markdown("#### 📈 Analytics")

        # Analytics button - full width
        if st.button(
            "📊 View Analytics", use_container_width=True, key="nav_analytics"
        ):
            st.session_state.page = "analytics"
            st.rerun()

        st.divider()

        # Quick stats
        try:
            expense_stats = expense_service.get_expense_stats()
            class_stats = class_service.get_class_stats()

            st.markdown("### 📊 Quick Stats")

            # Expenses
            expenses_html = f"""
                <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 4px; margin: 0.5rem 0;'>
                    <p style='color: white; font-size: 0.75rem; margin: 0;'>Total Expenses</p>
                    <p style='color: white; font-size: 1.25rem; font-weight: 700; margin: 0;'>
                        {expense_stats.total_expenses}
                    </p>
                </div>
            """
            st.markdown(expenses_html, unsafe_allow_html=True)

            # Spent
            spent_html = f"""
                <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 4px; margin: 0.5rem 0;'>
                    <p style='color: white; font-size: 0.75rem; margin: 0;'>Total Spent</p>
                    <p style='color: white; font-size: 1.25rem; font-weight: 700; margin: 0;'>
                        R$ {expense_stats.total_spent:,.2f}
                    </p>
                </div>
            """
            st.markdown(spent_html, unsafe_allow_html=True)

            # Revenue
            revenue_html = f"""
                <div style='background: rgba(255,255,255,0.1); padding: 0.75rem; border-radius: 4px; margin: 0.5rem 0;'>
                    <p style='color: white; font-size: 0.75rem; margin: 0;'>Class Revenue</p>
                    <p style='color: white; font-size: 1.25rem; font-weight: 700; margin: 0;'>
                        R$ {class_stats.total_revenue:,.2f}
                    </p>
                </div>
            """
            st.markdown(revenue_html, unsafe_allow_html=True)

            # Balance
            balance = class_stats.total_revenue - expense_stats.total_spent
            balance_color = (
                "rgba(16, 124, 16, 0.3)" if balance >= 0 else "rgba(209, 52, 56, 0.3)"
            )

            balance_html = f"""
                <div style='background: {balance_color}; padding: 0.75rem; border-radius: 4px; margin: 0.5rem 0;'>
                    <p style='color: white; font-size: 0.75rem; margin: 0;'>Balance</p>
                    <p style='color: white; font-size: 1.25rem; font-weight: 700; margin: 0;'>
                        R$ {abs(balance):,.2f}
                    </p>
                </div>
            """
            st.markdown(balance_html, unsafe_allow_html=True)

        except Exception:
            pass  # Silently fail for stats

        st.divider()

        # Footer
        st.markdown(
            """
            <p style='text-align: center; color: rgba(255,255,255,0.6); font-size: 0.75rem;'>
                © 2025 Personal Finance Manager
            </p>
            """,
            unsafe_allow_html=True,
        )


# ====================
# Main Application
# ====================
def main():
    """
    Main application function.
    Handles page routing and rendering.
    """
    # Apply permanent dark theme
    apply_fluent_theme()

    # Initialize session state for navigation
    if "page" not in st.session_state:
        st.session_state.page = "home"

    # Initialize services
    expense_service, class_service = init_services()

    # Show sidebar
    show_sidebar(expense_service, class_service)

    # Route to appropriate page
    current_page = st.session_state.page

    if current_page == "home":
        show_home_page(expense_service, class_service)

    elif current_page == "expenses":
        show_expenses_page(expense_service)

    elif current_page == "classes":
        show_classes_page(class_service)

    elif current_page == "analytics":
        show_analytics_page(expense_service, class_service)

    else:
        # Default to home if unknown page
        st.session_state.page = "home"
        st.rerun()


# ====================
# Run Application
# ====================
if __name__ == "__main__":
    main()
