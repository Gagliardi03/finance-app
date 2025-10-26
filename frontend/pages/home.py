import streamlit as st
from backend import ExpenseService, ClassService
from frontend.components import header_with_icon, metric_card


def show_home_page(expense_service: ExpenseService, class_service: ClassService):
    """
    Display home/dashboard page with overview and quick actions.
    All backgrounds are dark, text is white.

    Args:
        expense_service: Service for expense operations
        class_service: Service for class operations
    """
    # Page header with dark theme
    st.markdown(
        """
        <div style="text-align: center; padding: 48px 24px; background: #1a1a1a; 
                    border-radius: 12px; box-shadow: 0 6.4px 14.4px rgba(0, 0, 0, 0.5); 
                    margin-bottom: 48px; border: 1px solid #333333;">
            <h1 style="font-size: 32px; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                💰 Welcome to Your Financial Dashboard
            </h1>
            <p style="font-size: 16px; color: #e0e0e0; margin: 0;">
                Manage your finances and track your English classes all in one place.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ==================== QUICK ACTIONS ====================
    st.markdown(
        """
        <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
            🚀 Quick Actions
        </h2>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    # Action Card 1: Track Expenses
    with col1:
        st.markdown(
            """
            <div class="action-card">
                <div style="font-size: 48px; margin-bottom: 16px;">💸</div>
                <h3 style="color: #ffffff; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Track Expenses
                </h3>
                <p style="color: #e0e0e0; font-size: 14px; margin-bottom: 16px;">
                    Add and manage all your expenses
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Expenses", key="track_btn", use_container_width=True):
            st.session_state.page = "expenses"
            st.rerun()

    # Action Card 2: Analytics
    with col2:
        st.markdown(
            """
            <div class="action-card">
                <div style="font-size: 48px; margin-bottom: 16px;">📈</div>
                <h3 style="color: #ffffff; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Analytics
                </h3>
                <p style="color: #e0e0e0; font-size: 14px; margin-bottom: 16px;">
                    Visualize your spending patterns
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Analytics", key="analytics_btn", use_container_width=True):
            st.session_state.page = "analytics"
            st.rerun()

    # Action Card 3: Class Revenue
    with col3:
        st.markdown(
            """
            <div class="action-card">
                <div style="font-size: 48px; margin-bottom: 16px;">🎓</div>
                <h3 style="color: #ffffff; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                    Class Revenue
                </h3>
                <p style="color: #e0e0e0; font-size: 14px; margin-bottom: 16px;">
                    Track your teaching revenue
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Classes", key="classes_btn", use_container_width=True):
            st.session_state.page = "classes"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    # ==================== OVERVIEW ====================
    try:
        # Get statistics from services
        expense_stats = expense_service.get_expense_stats()
        class_stats = class_service.get_class_stats()

        st.markdown(
            """
            <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
                📊 Overview
            </h2>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        # Metric 1: Total Expenses
        with col1:
            metric_card(
                title="Total Expenses",
                value=str(expense_stats.total_expenses),
                icon="📝",
            )

        # Metric 2: Total Spent
        with col2:
            metric_card(
                title="Total Spent",
                value=f"R$ {expense_stats.total_spent:,.2f}",
                icon="💸",
            )

        # Metric 3: Total Classes
        with col3:
            metric_card(
                title="Total Classes",
                value=str(class_stats.total_classes),
                icon="📚",
            )

        # Metric 4: Class Revenue
        with col4:
            metric_card(
                title="Class Revenue",
                value=f"R$ {class_stats.total_revenue:,.2f}",
                icon="💰",
            )

        st.divider()

        # ==================== INSIGHTS ====================
        st.markdown(
            """
            <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
                💡 Insights
            </h2>
            """,
            unsafe_allow_html=True,
        )

        col1, col2 = st.columns(2)

        # Left insight: Spending
        with col1:
            if expense_stats.total_expenses > 0:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <h4 style="color: #ffffff; font-size: 16px; font-weight: 600; margin-bottom: 12px;">
                            💸 Spending Insights
                        </h4>
                        <div style="padding: 12px; background: #0f0f0f; border-radius: 6px; 
                                    margin-bottom: 8px; border-left: 3px solid #4da6ff;">
                            <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                      text-transform: uppercase; letter-spacing: 0.5px;">
                                Average Expense
                            </p>
                            <p style="color: #ffffff; font-size: 20px; font-weight: 700; margin: 4px 0 0 0;">
                                R$ {expense_stats.average_expense:,.2f}
                            </p>
                        </div>
                        <div style="padding: 12px; background: #0f0f0f; border-radius: 6px; 
                                    border-left: 3px solid #4da6ff;">
                            <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                      text-transform: uppercase; letter-spacing: 0.5px;">
                                Top Category
                            </p>
                            <p style="color: #ffffff; font-size: 16px; font-weight: 600; margin: 4px 0 0 0;">
                                {expense_stats.top_category}
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("🔭 No expense data yet. Start adding expenses!")

        # Right insight: Teaching
        with col2:
            if class_stats.total_classes > 0:
                st.markdown(
                    f"""
                    <div class="fluent-card">
                        <h4 style="color: #ffffff; font-size: 16px; font-weight: 600; margin-bottom: 12px;">
                            🎓 Teaching Insights
                        </h4>
                        <div style="padding: 12px; background: #0f0f0f; border-radius: 6px; 
                                    margin-bottom: 8px; border-left: 3px solid #4caf50;">
                            <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                      text-transform: uppercase; letter-spacing: 0.5px;">
                                Total Students
                            </p>
                            <p style="color: #ffffff; font-size: 20px; font-weight: 700; margin: 4px 0 0 0;">
                                {class_stats.student_count}
                            </p>
                        </div>
                        <div style="padding: 12px; background: #0f0f0f; border-radius: 6px; 
                                    border-left: 3px solid #4caf50;">
                            <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                      text-transform: uppercase; letter-spacing: 0.5px;">
                                Average per Class
                            </p>
                            <p style="color: #ffffff; font-size: 16px; font-weight: 600; margin: 4px 0 0 0;">
                                R$ {class_stats.average_per_class:,.2f}
                            </p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.info("🔭 No class data yet. Start adding classes!")

    except Exception as e:
        st.error(f"❌ Error loading dashboard data: {e}")
