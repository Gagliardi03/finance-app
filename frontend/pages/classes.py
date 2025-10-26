import streamlit as st
from backend import ClassService
from typing import List, Dict
from datetime import datetime
from io import BytesIO
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side


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

            st.markdown("<br>", unsafe_allow_html=True)

        # Action buttons
        col1, col2, col3 = st.columns(3)

        with col1:
            # Calculate total
            total_amount = sum(c["total"] for c in st.session_state.temp_classes)
            st.markdown(
                f"""
                <div style="padding: 12px; background: #1b3d1b; border-radius: 4px; 
                            border-left: 3px solid #4caf50; text-align: center; border: 1px solid #4caf50;">
                    <p style="color: #e0e0e0; font-size: 12px; margin: 0;">
                        Total Amount
                    </p>
                    <p style="color: #4caf50; font-size: 20px; font-weight: 700; margin: 4px 0 0 0;">
                        R$ {total_amount:,.2f}
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
                key="save_all_classes_btn",
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
                "🗑️ Clear All",
                use_container_width=True,
                key="clear_all_classes_btn",
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


def _create_formatted_classes_xlsx(df: pd.DataFrame) -> BytesIO:
    """
    Create a formatted Excel file for classes data.

    Args:
        df: DataFrame with classes data

    Returns:
        BytesIO buffer with formatted Excel file
    """
    try:
        # Create workbook and worksheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Classes"

        # Define styles
        header_font = Font(bold=True, color="FFFFFF", size=12)
        header_fill = PatternFill(
            start_color="4472C4", end_color="4472C4", fill_type="solid"
        )
        header_alignment = Alignment(horizontal="center", vertical="center")

        cell_alignment = Alignment(horizontal="left", vertical="center")
        number_alignment = Alignment(horizontal="right", vertical="center")

        border_style = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin"),
        )

        # Write title
        ws.merge_cells("A1:F1")
        title_cell = ws["A1"]
        title_cell.value = "English Classes Report"
        title_cell.font = Font(bold=True, size=16, color="1F4E78")
        title_cell.alignment = Alignment(horizontal="center", vertical="center")

        # Write headers
        headers = [
            "ID",
            "Date",
            "Student Name",
            "Class Value (R$)",
            "Quantity",
            "Total (R$)",
        ]
        for col_idx, header in enumerate(headers, 1):
            cell = ws.cell(row=3, column=col_idx)
            cell.value = header
            cell.font = header_font
            cell.fill = header_fill
            cell.alignment = header_alignment
            cell.border = border_style

        # Write data
        for row_idx, row_data in enumerate(df.itertuples(index=False), 4):
            ws.cell(row=row_idx, column=1, value=row_data.id).alignment = cell_alignment
            ws.cell(row=row_idx, column=2, value=str(row_data.date)[:10]).alignment = (
                cell_alignment
            )
            ws.cell(row=row_idx, column=3, value=row_data.student_name).alignment = (
                cell_alignment
            )
            ws.cell(row=row_idx, column=4, value=row_data.class_value).alignment = (
                number_alignment
            )
            ws.cell(row=row_idx, column=4).number_format = "R$ #,##0.00"
            ws.cell(row=row_idx, column=5, value=row_data.quantity).alignment = (
                number_alignment
            )
            ws.cell(row=row_idx, column=6, value=row_data.total).alignment = (
                number_alignment
            )
            ws.cell(row=row_idx, column=6).number_format = "R$ #,##0.00"

            # Apply borders
            for col_idx in range(1, 7):
                ws.cell(row=row_idx, column=col_idx).border = border_style

        # Add total row
        total_row = len(df) + 4
        ws.cell(row=total_row, column=1, value="TOTAL").font = Font(bold=True)
        ws.cell(row=total_row, column=1).alignment = cell_alignment
        ws.cell(row=total_row, column=6, value=df["total"].sum()).font = Font(bold=True)
        ws.cell(row=total_row, column=6).alignment = number_alignment
        ws.cell(row=total_row, column=6).number_format = "R$ #,##0.00"
        ws.cell(row=total_row, column=6).fill = PatternFill(
            start_color="E7E6E6", end_color="E7E6E6", fill_type="solid"
        )

        # Apply borders to total row
        for col_idx in range(1, 7):
            ws.cell(row=total_row, column=col_idx).border = border_style

        # Adjust column widths
        ws.column_dimensions["A"].width = 8
        ws.column_dimensions["B"].width = 15
        ws.column_dimensions["C"].width = 25
        ws.column_dimensions["D"].width = 18
        ws.column_dimensions["E"].width = 12
        ws.column_dimensions["F"].width = 18

        # Save to buffer
        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)

        return buffer

    except Exception as e:
        raise Exception(f"Error creating formatted Excel: {e}")


def _show_schedule_section(class_service: ClassService):
    """
    Display simple schedule/agenda for students.

    Args:
        class_service: Service for class operations
    """
    try:
        # Initialize schedule in session state
        if "student_schedule" not in st.session_state:
            st.session_state.student_schedule = []

        st.markdown("### 📅 Student Schedule")

        # Add schedule entry form
        with st.form("schedule_form", clear_on_submit=True):
            col1, col2, col3 = st.columns([3, 2, 1])

            with col1:
                schedule_student = st.text_input(
                    "Student Name", placeholder="e.g., John Smith"
                )

            with col2:
                schedule_time = st.text_input(
                    "Class Time", placeholder="e.g., Monday 10:00 AM"
                )

            with col3:
                st.write("")
                st.write("")
                add_schedule = st.form_submit_button("➕ Add", use_container_width=True)

            if add_schedule:
                if schedule_student and schedule_time:
                    st.session_state.student_schedule.append(
                        {"student": schedule_student, "time": schedule_time}
                    )
                    st.success(f"✅ Added: {schedule_student} - {schedule_time}")
                    st.rerun()
                else:
                    st.error("❌ Please fill in all fields!")

        # Display schedule
        if st.session_state.student_schedule:
            st.markdown("<br>", unsafe_allow_html=True)

            edit_idx = st.session_state.get("edit_schedule_idx", None)
            edit_data = st.session_state.get("edit_schedule_data", None)

            for idx, schedule_item in enumerate(st.session_state.student_schedule):
                col1, col2 = st.columns([5, 1])

                with col1:
                    st.markdown(
                        f"""
                        <div class=\"fluent-card\">
                            <div style=\"display: flex; justify-content: space-between; align-items: center;\">
                                <div>
                                    <p style=\"color: #ffffff; font-size: 16px; font-weight: 600; margin: 0;\">
                                        {schedule_item['student']}
                                    </p>
                                    <p style=\"color: #e0e0e0; font-size: 14px; margin: 4px 0 0 0;\">
                                        🕐 {schedule_item['time']}
                                    </p>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                with col2:
                    if st.button(
                        "🗑️",
                        key=f"del_schedule_{idx}",
                        help="Remove",
                        use_container_width=True,
                    ):
                        st.session_state.student_schedule.pop(idx)
                        st.rerun()

                    # Botão de editar abaixo da lixeira
                    if st.button(
                        "✏️",
                        key=f"edit_schedule_{idx}",
                        help="Edit schedule entry",
                        use_container_width=True,
                    ):
                        st.session_state.edit_schedule_idx = idx
                        st.session_state.edit_schedule_data = schedule_item.copy()
                        st.rerun()

                # Formulário de edição inline
                if edit_idx is not None and edit_data is not None and edit_idx == idx:
                    with st.form(f"edit_schedule_form_{idx}", clear_on_submit=True):
                        new_student = st.text_input(
                            "Student Name", value=edit_data["student"]
                        )
                        new_time = st.text_input("Class Time", value=edit_data["time"])
                        save = st.form_submit_button(
                            "💾 Save", use_container_width=True
                        )
                        cancel = st.form_submit_button(
                            "❌ Cancel", use_container_width=True
                        )
                        if save:
                            st.session_state.student_schedule[idx] = {
                                "student": new_student,
                                "time": new_time,
                            }
                            st.session_state.edit_schedule_idx = None
                            st.session_state.edit_schedule_data = None
                            st.success("Schedule updated!")
                            st.rerun()
                        elif cancel:
                            st.session_state.edit_schedule_idx = None
                            st.session_state.edit_schedule_data = None
                            st.info("Edit cancelled.")
                            st.rerun()

                st.markdown("<br>", unsafe_allow_html=True)
        else:
            st.info("📭 No schedule entries yet. Add your first entry above!")

    except Exception as e:
        st.error(f"❌ Error managing schedule: {e}")


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

        # Schedule section - REPLACE Top Students
        _show_schedule_section(class_service)

        st.divider()

        # Export section
        st.markdown("### 📥 Export Data")

        # Export formatted XLSX
        try:
            buffer = _create_formatted_classes_xlsx(df_classes)
            st.download_button(
                label="📊 Download Formatted Report (XLSX)",
                data=buffer,
                file_name=f"classes_report_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
        except Exception as e:
            st.error(f"❌ Error creating XLSX: {e}")

        st.divider()

        # Delete All section
        st.markdown("### 🗑️ Delete All Data")

        # Delete all button with confirmation
        if "show_delete_dialog_classes" not in st.session_state:
            st.session_state.show_delete_dialog_classes = False

        if not st.session_state.show_delete_dialog_classes:
            if st.button(
                "🗑️ Delete All Classes", type="secondary", use_container_width=True
            ):
                st.session_state.show_delete_dialog_classes = True
                st.rerun()

        # Confirmation dialog
        if st.session_state.show_delete_dialog_classes:
            st.warning(
                "⚠️ **Are you sure you want to delete ALL classes?** This action cannot be undone!"
            )

            col1, col2 = st.columns(2)
            with col1:
                if st.button(
                    "❌ Cancel",
                    key="cancel_delete_all_classes",
                    use_container_width=True,
                ):
                    st.session_state.show_delete_dialog_classes = False
                    st.rerun()
            with col2:
                if st.button(
                    "✅ Confirm Delete",
                    key="confirm_delete_all_classes",
                    type="primary",
                    use_container_width=True,
                ):
                    try:
                        class_service.delete_all_classes()
                        st.success("✅ All classes deleted successfully!")
                        st.session_state.show_delete_dialog_classes = False
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Error deleting classes: {e}")

    except Exception as e:
        st.error(f"❌ Error loading analytics: {e}")
