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


def _render_custom_tabs():
    """
    Render beautiful custom tab buttons with animations and hover effects.

    Returns:
        Selected tab name
    """
    # Initialize selected tab in session state
    if "analytics_selected_tab" not in st.session_state:
        st.session_state.analytics_selected_tab = "expenses"

    # Custom CSS for beautiful tabs
    st.markdown(
        """
        <style>
        .custom-tabs-container {
            display: flex;
            gap: 12px;
            padding: 16px 0;
            margin-bottom: 32px;
            justify-content: center;
        }
        
        .custom-tab-button {
            flex: 1;
            width: 100%;
            padding: 16px 24px;
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            border: 2px solid #333333;
            border-radius: 12px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            text-align: center;
            position: relative;
            overflow: hidden;
        }
        
        .custom-tab-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(77, 166, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .custom-tab-button:hover::before {
            left: 100%;
        }
        
        .custom-tab-button:hover {
            transform: translateY(-4px);
            border-color: #4da6ff;
            box-shadow: 0 8px 24px rgba(77, 166, 255, 0.3);
            background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
        }
        
        .custom-tab-button.active {
            background: linear-gradient(135deg, #4da6ff 0%, #357abd 100%);
            border-color: #4da6ff;
            box-shadow: 0 8px 24px rgba(77, 166, 255, 0.4);
            transform: translateY(-2px);
        }
        
        .custom-tab-button.active:hover {
            background: linear-gradient(135deg, #5bb0ff 0%, #4090d0 100%);
            transform: translateY(-4px);
        }
        
        .tab-icon {
            font-size: 28px;
            display: block;
            margin-bottom: 8px;
            filter: grayscale(50%);
            transition: all 0.3s ease;
        }
        
        .custom-tab-button:hover .tab-icon,
        .custom-tab-button.active .tab-icon {
            filter: grayscale(0%);
            transform: scale(1.1);
        }
        
        .tab-title {
            font-size: 16px;
            font-weight: 600;
            color: #e0e0e0;
            margin-bottom: 4px;
            transition: color 0.3s ease;
        }
        
        .custom-tab-button.active .tab-title {
            color: #ffffff;
        }
        
        .tab-description {
            font-size: 12px;
            color: #808080;
            transition: color 0.3s ease;
        }
        
        .custom-tab-button:hover .tab-description,
        .custom-tab-button.active .tab-description {
            color: #e0e0e0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Render custom tabs
    selected = st.session_state.analytics_selected_tab

    tabs_data = [
        {
            "id": "expenses",
            "icon": "💸",
            "title": "Expense Analytics",
            "description": "Track your spending",
        },
        {
            "id": "revenue",
            "icon": "🎓",
            "title": "Revenue Analytics",
            "description": "Monitor your income",
        },
        {
            "id": "combined",
            "icon": "📊",
            "title": "Combined View",
            "description": "Complete overview",
        },
    ]

    st.markdown('<div class="custom-tabs-container">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]

    for idx, tab in enumerate(tabs_data):
        with columns[idx]:
            active_class = "active" if selected == tab["id"] else ""

            st.markdown(
                f"""
                <div class="custom-tab-button {active_class}">
                    <span class="tab-icon">{tab["icon"]}</span>
                    <div class="tab-title">{tab["title"]}</div>
                    <div class="tab-description">{tab["description"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            if st.button(
                f"Select {tab['title']}",
                key=f"tab_{tab['id']}",
                use_container_width=True,
                type="secondary",
            ):
                st.session_state.analytics_selected_tab = tab["id"]
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    return st.session_state.analytics_selected_tab


def show_analytics_page(expense_service: ExpenseService, class_service: ClassService):
    """
    Display analytics page with charts and visualizations.
    Beautiful custom tabs for navigation.

    Args:
        expense_service: Service for expense operations
        class_service: Service for class operations
    """
    # Page header
    st.markdown(
        """
        <div style="text-align: center; padding: 32px 24px; background: #1a1a1a; 
                    border-radius: 12px; box-shadow: 0 6.4px 14.4px rgba(0, 0, 0, 0.5); 
                    margin-bottom: 32px; border: 1px solid #333333;">
            <h1 style="font-size: 32px; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                📈 Financial Analytics
            </h1>
            <p style="font-size: 16px; color: #e0e0e0; margin: 0;">
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
                            text-align: center; border: 2px dashed #404040;">
                    <div style="font-size: 64px; margin-bottom: 24px;">📊</div>
                    <h3 style="color: #e0e0e0; font-size: 20px; font-weight: 600; margin-bottom: 12px;">
                        No Data Available
                    </h3>
                    <p style="color: #808080; font-size: 14px; margin: 0;">
                        Start by adding expenses or classes to see analytics and visualizations.
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Custom beautiful tabs
        selected_tab = _render_custom_tabs()

        # ====================
        # TAB 1: Expense Analytics
        # ====================
        if selected_tab == "expenses":
            if not has_expense_data:
                st.markdown(
                    """
                    <div style="padding: 48px; background: #3d1b1b; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #f44336;">
                        <div style="font-size: 48px; margin-bottom: 16px;">💸</div>
                        <h3 style="color: #f44336; font-size: 18px; font-weight: 600; margin: 0;">
                            No Expense Data
                        </h3>
                        <p style="color: #e0e0e0; font-size: 14px; margin: 8px 0 0 0;">
                            Add some expenses to see expense analytics
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
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
                    <h3 style="font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
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
                    <h3 style="font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
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
        elif selected_tab == "revenue":
            if not has_class_data:
                st.markdown(
                    """
                    <div style="padding: 48px; background: #1b3d1b; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #4caf50;">
                        <div style="font-size: 48px; margin-bottom: 16px;">🎓</div>
                        <h3 style="color: #4caf50; font-size: 18px; font-weight: 600; margin: 0;">
                            No Revenue Data
                        </h3>
                        <p style="color: #e0e0e0; font-size: 14px; margin: 8px 0 0 0;">
                            Add some classes to see revenue analytics
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    """
                    <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
                        🎓 Revenue Analysis
                    </h2>
                    """,
                    unsafe_allow_html=True,
                )

                # Student analysis
                df_students = class_service.get_classes_by_student()

                if not df_students.empty:
                    st.markdown(
                        """
                        <h3 style="font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
                            👨‍🎓 Revenue by Student
                        </h3>
                        """,
                        unsafe_allow_html=True,
                    )

                    student_revenue_chart(
                        df_students, title="Revenue Breakdown by Student"
                    )

                    st.divider()

                    student_summary_table(df_students)

                st.divider()

                # Monthly revenue
                st.markdown(
                    """
                    <h3 style="font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
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

        # ====================
        # TAB 3: Combined View
        # ====================
        elif selected_tab == "combined":
            st.markdown(
                """
                <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
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
                    <h3 style="font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
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
                    <h3 style="font-size: 18px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
                        💰 Financial Summary
                    </h3>
                    """,
                    unsafe_allow_html=True,
                )

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown(
                        f"""
                        <div class="fluent-card" style="border-left: 4px solid #f44336;">
                            <div style="text-align: center;">
                                <div style="font-size: 32px; margin-bottom: 12px;">💸</div>
                                <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                          text-transform: uppercase; letter-spacing: 0.5px;">
                                    Total Expenses
                                </p>
                                <p style="color: #f44336; font-size: 28px; font-weight: 700; margin: 8px 0;">
                                    R$ {expense_stats.total_spent:,.2f}
                                </p>
                                <p style="color: #808080; font-size: 12px; margin: 0;">
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
                        <div class="fluent-card" style="border-left: 4px solid #4caf50;">
                            <div style="text-align: center;">
                                <div style="font-size: 32px; margin-bottom: 12px;">💰</div>
                                <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                          text-transform: uppercase; letter-spacing: 0.5px;">
                                    Total Revenue
                                </p>
                                <p style="color: #4caf50; font-size: 28px; font-weight: 700; margin: 8px 0;">
                                    R$ {class_stats.total_revenue:,.2f}
                                </p>
                                <p style="color: #808080; font-size: 12px; margin: 0;">
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
                    <div style="padding: 32px; background: #3d2d1b; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #ff9800;">
                        <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
                        <h3 style="color: #ff9800; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                            Partial Data
                        </h3>
                        <p style="color: #e0e0e0; font-size: 14px; margin: 0;">
                            Add some classes to see revenue data and complete financial overview
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif has_class_data:
                st.markdown(
                    """
                    <div style="padding: 32px; background: #3d2d1b; border-radius: 8px; 
                                text-align: center; border-left: 4px solid #ff9800;">
                        <div style="font-size: 48px; margin-bottom: 16px;">⚠️</div>
                        <h3 style="color: #ff9800; font-size: 18px; font-weight: 600; margin-bottom: 8px;">
                            Partial Data
                        </h3>
                        <p style="color: #e0e0e0; font-size: 14px; margin: 0;">
                            Add some expenses to see expense data and complete financial overview
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
