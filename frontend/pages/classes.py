import streamlit as st
from backend import ClassService
from frontend.components import (
    header_with_icon,
    class_form,
    class_table,
    metric_card,
    info_card,
    student_summary_table,
    student_revenue_chart,
)


def show_classes_page(class_service: ClassService):
    """
    Display classes page for viewing and adding English classes.

    Args:
        class_service: Service for class operations
    """
    # Page header
    header_with_icon("English Classes Management", "🎓", level=1)

    # Navigation buttons
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.divider()

    # Two-column layout
    col_form, col_list = st.columns([1, 1])

    # Left column: Add class form
    with col_form:
        st.markdown("### 📚 Register New Class")

        # Define callback function for form submission
        def handle_class_submit(student_name: str, class_value: float, quantity: int):
            """Handle class form submission"""
            class_service.create_class(
                student_name=student_name, class_value=class_value, quantity=quantity
            )

        # Display class form
        class_form(on_submit=handle_class_submit)

        st.divider()

        # Show quick stats
        try:
            stats = class_service.get_class_stats()

            if stats.total_classes > 0:
                st.markdown("### 📊 Quick Stats")

                metric_card(
                    title="Total Revenue",
                    value=f"R$ {stats.total_revenue:,.2f}",
                    icon="💰",
                )

                metric_card(
                    title="Total Classes",
                    value=str(stats.total_classes),
                    icon="📚",
                )

                metric_card(
                    title="Total Students",
                    value=str(stats.student_count),
                    icon="👥",
                )

                metric_card(
                    title="Avg per Class",
                    value=f"R$ {stats.average_per_class:,.2f}",
                    icon="📊",
                )

        except Exception as e:
            st.error(f"❌ Error loading stats: {e}")

    # Right column: Class list
    with col_list:
        st.markdown("### 📋 Recent Classes")

        try:
            # Get all classes
            df_classes = class_service.get_all_classes()

            if df_classes.empty:
                info_card(
                    title="No Classes Yet",
                    content="Start by adding your first class using the form on the left.",
                    card_type="info",
                    icon="📭",
                )
            else:
                # Show total count
                st.info(f"📊 **Total Records**: {len(df_classes)}")

                # Define callback for delete action
                def handle_delete(class_id: int):
                    """Handle class deletion"""
                    class_service.delete_class(class_id)

                # Display classes table
                class_table(df_classes, on_delete=handle_delete)

        except Exception as e:
            st.error(f"❌ Error loading classes: {e}")

    st.divider()

    # Student summary section
    try:
        df_students = class_service.get_classes_by_student()

        if not df_students.empty:
            st.markdown("## 👨‍🎓 Student Revenue Overview")

            # Display student summary table
            student_summary_table(df_students)

            st.divider()

            # Display revenue chart
            student_revenue_chart(df_students, title="Revenue by Student")

    except Exception as e:
        st.error(f"❌ Error loading student data: {e}")

    st.divider()

    # Export section
    try:
        df_classes = class_service.get_all_classes()

        if not df_classes.empty:
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
                df_students = class_service.get_classes_by_student()
                csv_summary = df_students.to_csv(index=False)

                st.download_button(
                    label="👥 Student Summary CSV",
                    data=csv_summary,
                    file_name="student_summary.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

    except Exception as e:
        pass  # Silently fail for export section
