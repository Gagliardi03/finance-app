import streamlit as st
from backend import ExpenseService, ClassService
from frontend.components import (
    header_with_icon,
    expense_pie_chart,
    expense_bar_chart,
    monthly_trend_chart,
    payment_method_chart,
    category_summary_table,
    info_card,
)


def show_analytics_page(expense_service: ExpenseService, class_service: ClassService):
    """
    Display analytics page with charts and visualizations.

    Args:
        expense_service: Service for expense operations
        class_service: Service for class operations
    """
    # Page header
    header_with_icon("Financial Analytics", "📈", level=1)

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
            info_card(
                title="No Data Available",
                content="Start by adding expenses or classes to see analytics and visualizations.",
                card_type="info",
                icon="📊",
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
                info_card(
                    title="No Expense Data",
                    content="Add some expenses to see expense analytics.",
                    card_type="info",
                    icon="💸",
                )
            else:
                st.markdown("## 💸 Expense Analysis")

                # Get category totals
                df_category = expense_service.get_expenses_by_category()

                # Two-column layout for charts
                col1, col2 = st.columns(2)

                with col1:
                    # Pie chart
                    expense_pie_chart(df_category, title="Spending by Category")

                with col2:
                    # Bar chart
                    expense_bar_chart(df_category, title="Category Breakdown")

                st.divider()

                # Payment method analysis
                st.markdown("### 💳 Payment Method Distribution")

                payment_dict = expense_service.get_expenses_by_payment_method()

                if payment_dict:
                    payment_method_chart(
                        payment_dict, title="Spending by Payment Method"
                    )
                else:
                    st.info("No payment method data available")

                st.divider()

                # Monthly trend
                st.markdown("### 📅 Monthly Spending Trend")

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
                info_card(
                    title="No Revenue Data",
                    content="Add some classes to see revenue analytics.",
                    card_type="info",
                    icon="🎓",
                )
            else:
                st.markdown("## 🎓 Revenue Analysis")

                # Get student data
                df_students = class_service.get_classes_by_student()

                # Display student summary
                from frontend.components import (
                    student_summary_table,
                    student_revenue_chart,
                )

                student_summary_table(df_students)

                st.divider()

                # Student revenue chart
                st.markdown("### 👥 Revenue by Student")
                student_revenue_chart(df_students, title="Student Revenue Breakdown")

                st.divider()

                # Monthly revenue trend
                st.markdown("### 📅 Monthly Revenue Trend")

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
                st.markdown("### 🏆 Top Students")

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
                                    <div>
                                        <span style="font-size: 1.5rem; margin-right: 1rem;">{emoji}</span>
                                        <strong style="font-size: 1.1rem; color: #323130;">
                                            {row['student_name']}
                                        </strong>
                                    </div>
                                    <div style="text-align: right;">
                                        <p style="color: #605e5c; font-size: 0.875rem; margin: 0;">
                                            {int(row['total_classes'])} classes
                                        </p>
                                        <p style="color: #107c10; font-size: 1.25rem; font-weight: 700; margin: 0;">
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
            st.markdown("## 📊 Combined Financial Overview")

            if has_expense_data and has_class_data:
                # Get totals
                expense_stats = expense_service.get_expense_stats()
                class_stats = class_service.get_class_stats()

                # Show comparison
                from frontend.components import comparison_chart

                comparison_chart(
                    expenses_total=expense_stats.total_spent,
                    revenue_total=class_stats.total_revenue,
                    title="Expenses vs Revenue",
                )

                st.divider()

                # Side-by-side monthly trends
                st.markdown("### 📅 Monthly Comparison")

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

                # Financial summary
                st.markdown("### 💰 Financial Summary")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown(
                        f"""
                        <div class="fluent-card">
                            <h4 style="color: #d13438; margin-bottom: 1rem;">💸 Total Expenses</h4>
                            <p style="font-size: 2rem; font-weight: 700; color: #d13438; margin: 0;">
                                R$ {expense_stats.total_spent:,.2f}
                            </p>
                            <p style="color: #605e5c; font-size: 0.875rem; margin-top: 0.5rem;">
                                {expense_stats.total_expenses} transactions
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:
                    st.markdown(
                        f"""
                        <div class="fluent-card">
                            <h4 style="color: #107c10; margin-bottom: 1rem;">💰 Total Revenue</h4>
                            <p style="font-size: 2rem; font-weight: 700; color: #107c10; margin: 0;">
                                R$ {class_stats.total_revenue:,.2f}
                            </p>
                            <p style="color: #605e5c; font-size: 0.875rem; margin-top: 0.5rem;">
                                {class_stats.total_classes} classes
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col3:
                    balance = class_stats.total_revenue - expense_stats.total_spent
                    balance_color = "#107c10" if balance >= 0 else "#d13438"
                    balance_icon = "✅" if balance >= 0 else "⚠️"

                    st.markdown(
                        f"""
                        <div class="fluent-card">
                            <h4 style="color: {balance_color}; margin-bottom: 1rem;">{balance_icon} Net Balance</h4>
                            <p style="font-size: 2rem; font-weight: 700; color: {balance_color}; margin: 0;">
                                R$ {abs(balance):,.2f}
                            </p>
                            <p style="color: #605e5c; font-size: 0.875rem; margin-top: 0.5rem;">
                                {'Positive' if balance >= 0 else 'Negative'}
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            elif has_expense_data:
                info_card(
                    title="Partial Data",
                    content="Add some classes to see revenue data and complete financial overview.",
                    card_type="warning",
                    icon="⚠️",
                )
            elif has_class_data:
                info_card(
                    title="Partial Data",
                    content="Add some expenses to see expense data and complete financial overview.",
                    card_type="warning",
                    icon="⚠️",
                )

    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
