import streamlit as st
from backend import ExpenseService, ClassService
from frontend.components import (
    expense_pie_chart,
    expense_bar_chart,
    monthly_trend_chart,
    payment_method_chart,
    category_summary_table,
    student_summary_table,
    student_revenue_chart,
    comparison_chart,
)


def show_analytics_page(expense_service: ExpenseService, class_service: ClassService):
    """
    Display analytics page with charts and visualizations.
    Following page.jsx design pattern.

    Args:
        expense_service: Service for expense operations
        class_service: Service for class operations
    """
    # Page header
    st.markdown(
        """
        <div style="text-align: center; padding: 32px 24px; background: #1a1a1a; 
                    border-radius: 12px; box-shadow: 0 6.4px 14.4px rgba(0, 0, 0, 0.132); 
                    margin-bottom: 32px;">
            <h1 style="font-size: 32px; font-weight: 700; color: #242424; margin-bottom: 8px;">
                📈 Financial Analytics
            </h1>
            <p style="font-size: 16px; color: #605e5c; margin: 0;">
                Comprehensive analysis of your financial data
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation buttons
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.divider()

    # Check if there's data to display
    try:
        df_expenses = expense_service.get_all_expenses()
        df_classes = class_service.get_all_classes()

        has_expense_data = not df_expenses.empty
        has_class_data = not df_classes.empty

        if not has_expense_data and not has_class_data:
            st.markdown(
                """
                <div style="padding: 64px; background: #1a1a1a; border-radius: 8px; 
                            text-align: center; border: 2px dashed #c8c6c4;">
                    <div style="font-size: 64px; margin-bottom: 24px;">📊</div>
                    <h3 style="color: #605e5c; font-size: 20px; font-weight: 600; margin-bottom: 12px;">
                        No Data Available
                    </h3>
                    <p style="color: #8a8886; font-size: 14px; margin: 0;">
                        Start by adding expenses or classes to see analytics and visualizations.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Tab navigation for different analytics sections
        tab1, tab2, tab3 = st.tabs(
            ["💸 Expense Analytics", "🎓 Revenue Analytics", "📊 Combined View"]
        )

        # ====================
        # TAB 1: Expense Analytics
        # ====================
        with tab1:
            if not has_expense_data:
                st.markdown(
                    """
                    <div style="padding: 48px; background: #fff4ce; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #f7630c;">
                        <div style="font-size: 48px; margin-bottom: 16px;">💸</div>
                        <h3 style="color: #8a5700; font-size: 18px; font-weight: 600; margin: 0;">
                            No Expense Data
                        </h3>
                        <p style="color: #8a5700; font-size: 14px; margin: 8px 0 0 0;">
                            Add some expenses to see expense analytics
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <h2 style="font-size: 24px; font-weight: 600; color: #242424; margin-bottom: 24px;">
                        💸 Expense Analysis
                    </h2>
                    """,
                    unsafe_allow_html=True,
                )

                # Get category totals
                df_category = expense_service.get_expenses_by_category()

                # Two-column layout for charts
                col1, col2 = st.columns(2)

                with col1:
                    expense_pie_chart(df_category, title="Spending by Category")

                with col2:
                    expense_bar_chart(df_category, title="Category Breakdown")

                st.divider()

                # Payment method analysis
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        💳 Payment Method Distribution
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                payment_dict = expense_service.get_expenses_by_payment_method()

                if payment_dict:
                    payment_method_chart(
                        payment_dict, title="Spending by Payment Method"
                    )
                else:
                    st.info("No payment method data available")

                st.divider()

                # Monthly trend
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        📅 Monthly Spending Trend
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                df_monthly = expense_service.get_monthly_expenses()

                if not df_monthly.empty:
                    monthly_trend_chart(
                        df_monthly, title="Monthly Expenses", y_label="Total Spent (R$)"
                    )
                else:
                    st.info("Not enough data for monthly trends")

                st.divider()

                # Category summary table
                category_summary_table(df_category)

        # ====================
        # TAB 2: Revenue Analytics
        # ====================
        with tab2:
            if not has_class_data:
                st.markdown(
                    """
                    <div style="padding: 48px; background: #fff4ce; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #f7630c;">
                        <div style="font-size: 48px; margin-bottom: 16px;">🎓</div>
                        <h3 style="color: #8a5700; font-size: 18px; font-weight: 600; margin: 0;">
                            No Revenue Data
                        </h3>
                        <p style="color: #8a5700; font-size: 14px; margin: 8px 0 0 0;">
                            Add some classes to see revenue analytics
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <h2 style="font-size: 24px; font-weight: 600; color: #242424; margin-bottom: 24px;">
                        🎓 Revenue Analysis
                    </h2>
                    """,
                    unsafe_allow_html=True,
                )

                # Get student data
                df_students = class_service.get_classes_by_student()

                # Display student summary
                student_summary_table(df_students)

                st.divider()

                # Student revenue chart
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        👥 Revenue by Student
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )
                student_revenue_chart(df_students, title="Student Revenue Breakdown")

                st.divider()

                # Monthly revenue trend
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        📅 Monthly Revenue Trend
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                df_monthly_revenue = class_service.get_monthly_revenue()

                if not df_monthly_revenue.empty:
                    monthly_trend_chart(
                        df_monthly_revenue,
                        title="Monthly Revenue",
                        y_label="Revenue (R$)",
                    )
                else:
                    st.info("Not enough data for monthly trends")

                st.divider()

                # Top students
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        🏆 Top Students
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                df_top = class_service.get_top_students(limit=5)

                if not df_top.empty:
                    for idx, row in df_top.iterrows():
                        rank = idx + 1
                        emoji = (
                            "🥇"
                            if rank == 1
                            else "🥈" if rank == 2 else "🥉" if rank == 3 else "⭐"
                        )

                        st.markdown(
                            f"""
                            <div class="fluent-card">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div style="display: flex; align-items: center; gap: 16px;">
                                        <span style="font-size: 32px;">{emoji}</span>
                                        <div>
                                            <p style="color: #605e5c; font-size: 12px; margin: 0; 
                                                      text-transform: uppercase; letter-spacing: 0.5px;">
                                                Rank #{rank}
                                            </p>
                                            <p style="color: #242424; font-size: 18px; font-weight: 600; margin: 4px 0 0 0;">
                                                {row['student_name']}
                                            </p>
                                        </div>
                                    </div>
                                    <div style="text-align: right;">
                                        <p style="color: #605e5c; font-size: 12px; margin: 0;">
                                            {int(row['total_classes'])} classes
                                        </p>
                                        <p style="color: #107c10; font-size: 20px; font-weight: 700; margin: 4px 0 0 0;">
                                            R$ {row['total_revenue']:,.2f}
                                        </p>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )
                else:
                    st.info("No student data available")

        # ====================
        # TAB 3: Combined View
        # ====================
        with tab3:
            st.markdown(
                """
                <h2 style="font-size: 24px; font-weight: 600; color: #242424; margin-bottom: 24px;">
                    📊 Combined Financial Overview
                </h2>
                """,
                unsafe_allow_html=True,
            )

            if has_expense_data and has_class_data:
                # Get totals
                expense_stats = expense_service.get_expense_stats()
                class_stats = class_service.get_class_stats()

                # Show comparison
                comparison_chart(
                    expenses_total=expense_stats.total_spent,
                    revenue_total=class_stats.total_revenue,
                    title="Expenses vs Revenue",
                )

                st.divider()

                # Side-by-side monthly trends
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        📅 Monthly Comparison
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)

                with col1:
                    df_monthly_expenses = expense_service.get_monthly_expenses()
                    if not df_monthly_expenses.empty:
                        monthly_trend_chart(
                            df_monthly_expenses,
                            title="Monthly Expenses",
                            y_label="Spent (R$)",
                        )
                    else:
                        st.info("No monthly expense data")

                with col2:
                    df_monthly_revenue = class_service.get_monthly_revenue()
                    if not df_monthly_revenue.empty:
                        monthly_trend_chart(
                            df_monthly_revenue,
                            title="Monthly Revenue",
                            y_label="Revenue (R$)",
                        )
                    else:
                        st.info("No monthly revenue data")

                st.divider()

                # Financial summary with beautiful cards
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #242424; margin-bottom: 16px;">
                        💰 Financial Summary
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        f"""
                        <div class="fluent-card" style="border-left: 4px solid #d13438;">
                            <div style="text-align: center;">
                                <div style="font-size: 32px; margin-bottom: 12px;">💸</div>
                                <p style="color: #605e5c; font-size: 12px; margin: 0; 
                                          text-transform: uppercase; letter-spacing: 0.5px;">
                                    Total Expenses
                                </p>
                                <p style="color: #d13438; font-size: 28px; font-weight: 700; margin: 8px 0;">
                                    R$ {expense_stats.total_spent:,.2f}
                                </p>
                                <p style="color: #605e5c; font-size: 12px; margin: 0;">
                                    {expense_stats.total_expenses} transactions
                                </p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="fluent-card" style="border-left: 4px solid #107c10;">
                            <div style="text-align: center;">
                                <div style="font-size: 32px; margin-bottom: 12px;">💰</div>
                                <p style="color: #605e5c; font-size: 12px; margin: 0; 
                                          text-transform: uppercase; letter-spacing: 0.5px;">
                                    Total Revenue
                                </p>
                                <p style="color: #107c10; font-size: 28px; font-weight: 700; margin: 8px 0;">
                                    R$ {class_stats.total_revenue:,.2f}
                                </p>
                                <p style="color: #605e5c; font-size: 12px; margin: 0;">
                                    {class_stats.total_classes} classes
                                </p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            elif has_expense_data:
                st.markdown(
                    """
                    <div style="padding: 32px; background: #fff4ce; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #f7630c;">
                        <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
                        <h3 style="color: #8a5700; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                            Partial Data
                        </h3>
                        <p style="color: #8a5700; font-size: 14px; margin: 0;">
                            Add some classes to see revenue data and complete financial overview
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif has_class_data:
                st.markdown(
                    """
                    <div style="padding: 32px; background: #fff4ce; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #f7630c;">
                        <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
                        <h3 style="color: #8a5700; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                            Partial Data
                        </h3>
                        <p style="color: #8a5700; font-size: 14px; margin: 0;">
                            Add some expenses to see expense data and complete financial overview
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
