import streamlit as st
from backend import ClassService
from typing import List, Dict
from datetime import datetime


def show_classes_page(class_service: ClassService):
    """
    Display classes page for adding English classes.
    New flow: Add multiple classes, then save all at once.
    View analytics in a separate view.
    DARK MODE PERMANENT.

    Args:
        class_service: Service for class operations
    """
    # Initialize session state for temporary classes
    if "temp_classes" not in st.session_state:
        st.session_state.temp_classes = []
    if "show_class_analytics" not in st.session_state:
        st.session_state.show_class_analytics = False

    # Page header - DARK
    st.markdown(
        """
        <div style="text-align: center; padding: 32px 24px; background: #1a1a1a; 
                    border-radius: 12px; box-shadow: 0 6.4px 14.4px rgba(0, 0, 0, 0.5); 
                    margin-bottom: 32px; border: 1px solid #333333;">
            <h1 style="font-size: 32px; font-weight: 700; color: #ffffff; margin-bottom: 8px;">
                🎓 English Classes Management
            </h1>
            <p style="font-size: 16px; color: #e0e0e0; margin: 0;">
                Track your teaching revenue and manage classes
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Navigation buttons
    col1, col2, col3 = st.columns([1, 1, 4])
    with col1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.session_state.show_class_analytics = False
            st.rerun()
    with col2:
        analytics_label = (
            "📝 Add Classes"
            if st.session_state.show_class_analytics
            else "📊 View Analytics"
        )
        if st.button(analytics_label, use_container_width=True):
            st.session_state.show_class_analytics = (
                not st.session_state.show_class_analytics
            )
            st.rerun()

    st.divider()

    # ==================== ANALYTICS VIEW ====================
    if st.session_state.show_class_analytics:
        _show_analytics_view(class_service)
        return

    # ==================== ADD CLASSES VIEW ====================
    _show_add_classes_view(class_service)


def _show_add_classes_view(class_service: ClassService):
    """
    Show the view for adding classes.
    DARK MODE PERMANENT.

    Args:
        class_service: Service for class operations
    """
    # ==================== ADD CLASS FORM ====================
    st.markdown(
        """
        <h2 style="font-size: 20px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
            📚 Register New Class
        </h2>
        """,
        unsafe_allow_html=True,
    )

    with st.form("class_form", clear_on_submit=True):
        col1, col2, col3 = st.columns(3)

        with col1:
            # Student name
            student_name = st.text_input(
                "Student Name",
                placeholder="e.g., John Smith",
                help="Name of the student",
            )

        with col2:
            # Class value
            class_value = st.number_input(
                "Class Value (BRL)",
                min_value=0.01,
                step=0.01,
                format="%.2f",
                help="Price per class",
            )

        with col3:
            # Quantity
            quantity = st.number_input(
                "Number of Classes",
                min_value=1,
                step=1,
                value=1,
                help="How many classes?",
            )

        # Show total - DARK
        total = class_value * quantity
        st.markdown(
            f"""
            <div style="padding: 12px; background: #1b3d1b; border-radius: 4px; 
                        border-left: 3px solid #4caf50; margin-top: 16px; border: 1px solid #4caf50;">
                <p style="color: #4caf50; font-size: 14px; font-weight: 600; margin: 0;">
                    💰 Total Amount: R$ {total:,.2f}
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Submit button
        submitted = st.form_submit_button(
            "➕ Add to List", use_container_width=True, type="primary"
        )

        if submitted:
            # Validate inputs
            if not student_name or not student_name.strip():
                st.error("❌ Please enter student name!")
            else:
                # Add to temporary list
                temp_class = {
                    "student_name": student_name.strip(),
                    "class_value": class_value,
                    "quantity": quantity,
                    "total": total,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                st.session_state.temp_classes.append(temp_class)
                st.success(
                    f"✅ Added: {quantity} class(es) for {student_name} - R$ {total:,.2f}"
                )
                st.rerun()

    st.divider()

    # ==================== TEMPORARY CLASSES LIST ====================
    if st.session_state.temp_classes:
        st.markdown(
            f"""
            <h2 style="font-size: 20px; font-weight: 600; color: #ffffff; margin-bottom: 16px;">
                📋 Classes to Save ({len(st.session_state.temp_classes)})
            </h2>
            """,
            unsafe_allow_html=True,
        )

        # Display classes in table format
        for idx, class_data in enumerate(st.session_state.temp_classes):
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

            with col1:
                st.markdown(
                    f"""
                    <div style="padding: 8px; background: #2d2d2d; border-radius: 4px; border: 1px solid #404040;">
                        <p style="color: #e0e0e0; font-size: 10px; margin: 0; 
                                  text-transform: uppercase; letter-spacing: 0.5px;">
                            Student
                        </p>
                        <p style="color: #ffffff; font-size: 14px; font-weight: 600; margin: 4px 0 0 0;">
                            {class_data['student_name']}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col2:
                st.markdown(
                    f"""
                    <div style="padding: 8px; background: #2d2d2d; border-radius: 4px; border: 1px solid #404040;">
                        <p style="color: #e0e0e0; font-size: 10px; margin: 0; 
                                  text-transform: uppercase; letter-spacing: 0.5px;">
                            Class Value
                        </p>
                        <p style="color: #ffffff; font-size: 14px; font-weight: 600; margin: 4px 0 0 0;">
                            R$ {class_data['class_value']:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col3:
                st.markdown(
                    f"""
                    <div style="padding: 8px; background: #2d2d2d; border-radius: 4px; border: 1px solid #404040;">
                        <p style="color: #e0e0e0; font-size: 10px; margin: 0; 
                                  text-transform: uppercase; letter-spacing: 0.5px;">
                            Quantity
                        </p>
                        <p style="color: #ffffff; font-size: 14px; font-weight: 600; margin: 4px 0 0 0;">
                            {class_data['quantity']} classes
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col4:
                st.markdown(
                    f"""
                    <div style="padding: 8px; background: #2d2d2d; border-radius: 4px; border: 1px solid #404040;">
                        <p style="color: #e0e0e0; font-size: 10px; margin: 0; 
                                  text-transform: uppercase; letter-spacing: 0.5px;">
                            Total
                        </p>
                        <p style="color: #4caf50; font-size: 14px; font-weight: 700; margin: 4px 0 0 0;">
                            R$ {class_data['total']:,.2f}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with col5:
                if st.button(
                    "🗑️",
                    key=f"del_temp_cls_{idx}",
                    help="Remove from list",
                    use_container_width=True,
                ):
                    st.session_state.temp_classes.pop(idx)
                    st.success("✅ Removed!")
                    st.rerun()

            st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons
        st.divider()

        col1, col2, col3 = st.columns([2, 2, 2])

        with col1:
            # Calculate total
            total = sum(cls["total"] for cls in st.session_state.temp_classes)
            st.markdown(
                f"""
                <div style="padding: 16px; background: #2d2d2d; border-radius: 6px; 
                            text-align: center; border-left: 4px solid #4caf50; border: 1px solid #404040;">
                    <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                              text-transform: uppercase; letter-spacing: 0.5px;">
                        Total Revenue
                    </p>
                    <p style="color: #4caf50; font-size: 24px; font-weight: 700; margin: 4px 0 0 0;">
                        R$ {total:,.2f}
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col2:
            if st.button(
                "💾 Save All Classes",
                use_container_width=True,
                type="primary",
                key="save_all_cls_btn",
            ):
                try:
                    # Save all classes to database
                    for class_data in st.session_state.temp_classes:
                        class_service.create_class(
                            student_name=class_data["student_name"],
                            class_value=class_data["class_value"],
                            quantity=class_data["quantity"],
                        )

                    # Clear temporary list
                    count = len(st.session_state.temp_classes)
                    st.session_state.temp_classes = []

                    st.success(f"✅ Successfully saved {count} class(es)!")
                    st.balloons()
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error saving classes: {e}")

        with col3:
            if st.button(
                "🗑️ Clear All", use_container_width=True, key="clear_all_cls_btn"
            ):
                st.session_state.temp_classes = []
                st.success("✅ List cleared!")
                st.rerun()

    else:
        st.markdown(
            """
            <div style="padding: 48px; background: #1a1a1a; border-radius: 8px; 
                        text-align: center; border: 2px dashed #404040;">
                <div style="font-size: 48px; margin-bottom: 16px;">📭</div>
                <h3 style="color: #e0e0e0; font-size: 18px; font-weight: 600; margin: 0;">
                    No classes added yet
                </h3>
                <p style="color: #808080; font-size: 14px; margin: 8px 0 0 0;">
                    Use the form above to add your first class
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


def _show_analytics_view(class_service: ClassService):
    """
    Show analytics and visualizations for classes.
    DARK MODE PERMANENT.

    Args:
        class_service: Service for class operations
    """
    from frontend.components import (
        student_summary_table,
        student_revenue_chart,
        monthly_trend_chart,
        metric_card,
    )

    st.markdown(
        """
        <h2 style="font-size: 24px; font-weight: 600; color: #ffffff; margin-bottom: 24px;">
            📊 Revenue Analytics
        </h2>
        """,
        unsafe_allow_html=True,
    )

    # Botão de exclusão total com confirmação
    if "show_delete_dialog_classes" not in st.session_state:
        st.session_state.show_delete_dialog_classes = False
    if st.button("🗑️ Delete All Classes", type="primary", use_container_width=True):
        st.session_state.show_delete_dialog_classes = True
    if st.session_state.show_delete_dialog_classes:
        st.warning(
            "Are you sure you want to delete ALL classes? This action cannot be undone!"
        )
        col1, col2 = st.columns(2)
        with col1:
            if st.button("❌ Cancel", key="cancel_delete_all_classes"):
                st.session_state.show_delete_dialog_classes = False
        with col2:
            if st.button("✅ Confirm Delete", key="confirm_delete_all_classes"):
                try:
                    class_service.delete_all_classes()
                    st.success("All classes deleted!")
                    st.session_state.show_delete_dialog_classes = False
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting classes: {e}")

    try:
        # Get data
        df_classes = class_service.get_all_classes()

        if df_classes.empty:
            st.markdown(
                """
                <div style="padding: 48px; background: #1a1a1a; border-radius: 8px; 
                            text-align: center; border: 2px dashed #404040;">
                    <div style="font-size: 48px; margin-bottom: 16px;">📊</div>
                    <h3 style="color: #e0e0e0; font-size: 18px; font-weight: 600; margin: 0;">
                        No class data available
                    </h3>
                    <p style="color: #808080; font-size: 14px; margin: 8px 0 0 0;">
                        Add some classes to see analytics and visualizations
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            return

        # Quick Stats
        stats = class_service.get_class_stats()

        st.markdown("### 📈 Quick Stats")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            metric_card(
                title="Total Revenue",
                value=f"R$ {stats.total_revenue:,.2f}",
                icon="💰",
            )

        with col2:
            metric_card(
                title="Total Classes", value=str(stats.total_classes), icon="📚"
            )

        with col3:
            metric_card(
                title="Total Students", value=str(stats.student_count), icon="👥"
            )

        with col4:
            metric_card(
                title="Avg per Class",
                value=f"R$ {stats.average_per_class:,.2f}",
                icon="📊",
            )

        st.divider()

        # Student Analysis
        df_students = class_service.get_classes_by_student()

        if not df_students.empty:
            st.markdown("### 👨‍🎓 Student Revenue Overview")
            student_summary_table(df_students)

            st.divider()

            # Revenue chart
            st.markdown("### 💰 Revenue by Student")
            student_revenue_chart(df_students, title="Revenue Breakdown by Student")

            st.divider()

        # Monthly revenue trend
        st.markdown("### 📅 Monthly Revenue Trend")

        df_monthly_revenue = class_service.get_monthly_revenue()

        if not df_monthly_revenue.empty:
            monthly_trend_chart(
                df_monthly_revenue, title="Monthly Revenue", y_label="Revenue (R$)"
            )
        else:
            st.info("Not enough data for monthly trends")

        st.divider()

        # Top Students - DARK
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
                            <div style="display: flex; align-items: center; gap: 16px;">
                                <span style="font-size: 32px;">{emoji}</span>
                                <div>
                                    <p style="color: #e0e0e0; font-size: 12px; margin: 0; 
                                              text-transform: uppercase; letter-spacing: 0.5px;">
                                        Rank #{rank}
                                    </p>
                                    <p style="color: #ffffff; font-size: 18px; font-weight: 600; margin: 4px 0 0 0;">
                                        {row['student_name']}
                                    </p>
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <p style="color: #e0e0e0; font-size: 12px; margin: 0;">
                                    {int(row['total_classes'])} classes
                                </p>
                                <p style="color: #4caf50; font-size: 20px; font-weight: 700; margin: 4px 0 0 0;">
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

        st.divider()

        # Export section
        st.markdown("### 📥 Export Data")

        col1, col2, col3 = st.columns(3)

        with col1:
            # Export to CSV
            csv = df_classes.to_csv(index=False)
            st.download_button(
                label="📄 Download as CSV",
                data=csv,
                file_name="classes.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col2:
            # Export to Excel
            from io import BytesIO

            buffer = BytesIO()
            df_classes.to_excel(buffer, index=False, engine="openpyxl")
            buffer.seek(0)

            st.download_button(
                label="📊 Download as Excel",
                data=buffer,
                file_name="classes.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

        with col3:
            # Export student summary
            csv_summary = df_students.to_csv(index=False)

            st.download_button(
                label="👥 Student Summary CSV",
                data=csv_summary,
                file_name="student_summary.csv",
                mime="text/csv",
                use_container_width=True,
            )

    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
